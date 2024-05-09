import modal
import os
import subprocess
import time

from modal import build, enter, method

MODEL = os.environ.get("MODEL", "llama3:instruct")

def pull(model: str = MODEL):
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ollama"])
    subprocess.run(["systemctl", "start", "ollama"])
    time.sleep(2)  # 2s, wait for the service to start
    subprocess.run(["ollama", "pull", model], stdout=subprocess.PIPE)

image = (
    modal.Image
    .debian_slim()
    .apt_install("curl", "systemctl")
    .run_commands( # from https://github.com/ollama/ollama/blob/main/docs/linux.md
        "curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama",
        "chmod +x /usr/bin/ollama",
        "useradd -r -s /bin/false -m -d /usr/share/ollama ollama",
    )
    .copy_local_file("ollama.service", "/etc/systemd/system/ollama.service")
    .pip_install("ollama")
    .run_function(pull)
)

app = modal.App(name="ollama", image=image)

with image.imports():
    import ollama

@app.cls(gpu="a10g", region="us-east", container_idle_timeout=300)
class Ollama:
    @build()
    def pull(self):
        # TODO(irfansharif): Was hoping that the following would use an image
        # with this explicit @build() step's results, but alas, it doesn't - so
        # we're baking it directly into the base image above. Also, would be
        # nice to simply specify the class name? Not like the method is
        # specified has any relevance.
        #
        #  $ modal shell ollama-modal.py::Ollama.infer

        # pull(model=MODEL)
        ...

    @enter()
    def load(self):
        subprocess.run(["systemctl", "start", "ollama"])

    @method()
    def infer(self, text: str):
        stream = ollama.chat(
            model=MODEL,
            messages=[{'role': 'user', 'content': text}],
            stream=True
        )
        for chunk in stream:
            yield chunk['message']['content']
            print(chunk['message']['content'], end='', flush=True)
        return

# Convenience thing, to run using:
#
#  $ modal run ollama-modal.py [--lookup] [--text "Why is the sky blue?"]
@app.local_entrypoint()
def main(text: str = "Why is the sky blue?", lookup: bool = False):
    if lookup:
        ollama = modal.Cls.lookup("ollama", "Ollama")
    else:
        ollama = Ollama()
    for chunk in ollama.infer.remote_gen(text):
        print(chunk, end='', flush=False)
