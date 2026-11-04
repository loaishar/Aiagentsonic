# Aiagentsonic

A personal adaptation of the MIT-licensed OpenManus agent framework. The code includes tool-calling agents, planning flows, browser automation, search tools, and MCP integrations. See [UPSTREAM.md](UPSTREAM.md) for attribution.

This is a source-code portfolio repository, not a hosted service. The original framework is credited to its upstream authors; publishing this adaptation does not claim authorship of OpenManus.

## Local setup

Use Python 3.12 in an isolated environment:

```sh
python -m venv .venv
# Activate .venv using your shell's activation command.
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Copy `config/config.example.toml` to `config/config.toml`. Supply your own model, provider endpoint, and API key only in that ignored local file. The committed configuration contains an empty API-key placeholder. No credentials or paid API calls are supplied by this repository.

Once configured, the original entry points are `python main.py`, `python run_flow.py`, and `python run_mcp_server.py`. Installing dependencies and running live integrations were not part of the privacy cleanup; compatibility and live inference have not been verified for this snapshot.

## Privacy and execution

This clean publication excludes the old repository's history, logs, generated workspace files, screenshots, setup notes, and original documentation. Only selected source files, dependency declarations, original licensing, placeholder configuration, and these new public instructions are included.

Agents can execute code, access files, and browse the network. Run only in a disposable environment without personal data, saved browser sessions, cloud credentials, or production access. The framework's optional sandbox setting does not make every tool isolated. Review [SECURITY.md](SECURITY.md) before use.

The privacy cleanup was checked with a full Git-history secret scan and Python syntax parsing. These checks do not establish runtime correctness or the absence of every possible sensitive item.
