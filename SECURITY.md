# Security and private configuration

- Commit empty credential placeholders only. Keep provider keys in the ignored `config/config.toml` or other ignored local configuration.
- Never commit logs, generated documents, browser profiles, customer data, account exports, tokens, private keys, or connection strings containing passwords.
- `.gitignore` does not protect files already tracked. Inspect staged changes and run a secret scanner before pushing.
- Docker build context excludes local credentials and generated output. Keep credentials outside images.
- This agent framework includes shell, Python, browser, and file tools. Use a disposable environment with least privilege; do not connect a personal browser profile or expose an unauthenticated tool server to the Internet.
- If a credential was previously published, revoke or rotate it at the provider. A clean publication cannot revoke a secret, erase external copies, or remove provider-side access.

The public snapshot was scanned before publication. No real provider key was used or tested during cleanup. Live model calls, dependencies, and tool isolation were not security-audited as part of this privacy cleanup.
