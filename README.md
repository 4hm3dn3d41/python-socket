
# Socket File Transfer Project

A simple Python file transfer project that demonstrates core networking, checksum, and encryption concepts using sockets. It supports both secure and unsecure file transfers between a client and a server.

## Features

* Secure transfers using ChaCha20
* Unsecure (plain) file transfers
* File listing from the server
* SHA-256 integrity verification

## Structure

* `client_soc.py` – Client downloader
* `multi_sevrer_soc.py` – Multi-client server
* `storage/` – Server files
* `folder/` – Client downloads (auto-created)

## Usage

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:

```bash
python multi_sevrer_soc.py
```

4. Run the client:

```bash
python client_soc.py
```

Choose secure (`y`) or unsecure (`n`), select a file, and it downloads to `folder/`.

## Notes

* Default host: `127.0.0.1`
* Ports:

  * Secure: `53189`
  * Unsecure: `56723`
* Requires Python 3.x and `pycryptodomex`
