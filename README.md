    
    # To get an Ollama prompt, running on Modal.
    $ modal shell --region us-east ollama-modal.py \
        --cmd 'systemctl start ollama && ollama run llama3:instruct'
    >>> Send a message (/? for help)

<img width="1278" alt="image" src="https://github.com/irfansharif/ollama-modal/assets/10536690/197a1aa4-36f8-47b4-9efc-76bffe03896a">

    # For one-off things.
    modal run ollama-modal.py [--text "Why is the sky blue?"] [--lookup]

    # If using --lookup, first deploy.
    modal deploy ollama-modal.py

    # MODEL=... can be used to control what ollama model we bake into
    # underlying images, defaulting to llama3:instruct (8b). See from
    # https://ollama.com/library for other options.
