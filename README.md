# pr-review
pr-review

## What it does
This is a simple pr-review mechanism leveraging the capabilities of AI to review the changes in a PR.
It compares the last commit with the one before that, identifies the changes and recommends code improvments on the changed code.


## How to use
1. In config.yaml, update the location of the directory holding the code
2. In .env, update the openai key, with the key, "OPENAI_KEY=XYZ"
3. Run python3 main.py to view the suggestions by openai 