    
    # To get an Ollama prompt, running on Modal.
    $ modal shell --region us-east ollama-modal.py
    root@modal:/# systemctl start ollama
    root@modal:/# ollama run llama3:instruct
    >>> Send a message (/? for help)

    # For one-off things.
    modal run ollama-modal.py [--text "Why is the sky blue?"] [--lookup]

    # If using --lookup, first deploy.
    modal deploy ollama-modal.py

    # MODEL=... can be used to control what ollama model we bake into
    # underlying images, defaulting to llama3:instruct (8b). See from
    # https://ollama.com/library for other options.
