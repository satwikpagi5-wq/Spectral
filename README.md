# The Spectral Terminal & Ofrenda Chamber

A local-first tribute to the people, machines, languages, and open-source projects that leave traces behind. The **Virtual Ofrenda** lets you remember loved ones, technology pioneers, and forgotten software with candlelight, offerings, photos, and stories. The **Haunted Séance Terminal** lets you summon COBOL, FORTRAN, x86 Assembly, early Unix, Netscape, Gemma, or Llama for eerie, technical conversation.

## Run locally

Requires Python 3.9+. No packages, build step, account, or internet connection are required to run the app itself.

```powershell
python server.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Keep the local server running. The altar, candle and offering interactions, memory box, and deterministic terminal oracle work without Ollama or internet access.

## Summon an open-weight model

Install [Ollama](https://ollama.com), then download a small local model once:

```powershell
ollama pull gemma3:1b
```

Keep Ollama running and open **Local AI & settings** to confirm the connection. You can select another installed model by entering its Ollama model name. The terminal sends its prompt only to the local Python server, which forwards it to Ollama at `127.0.0.1:11434`. The remembrance writer sends only the name, relationship, and chosen text details; it never sends attached photos. If Ollama is unavailable, the deterministic persona oracle answers instead.

Ollama's initial model download needs internet. Afterward, local inference and the cached app shell can run offline while the local server and Ollama remain running. No Google Fonts, icon CDN, hosted AI API, or other external asset is used.

## Privacy

- People, offerings, memories, photos, and candle counts are saved in this browser's IndexedDB on this device.
- There are no accounts, analytics, hosted database, or telemetry.
- AI requests are optional and go to the local Ollama service on this computer. Model responses are fictional creative output, not messages from a deceased person or conscious program.
- Export a JSON backup from the arrow button or settings. It includes photos and is unencrypted, so keep it private. Browser storage is not a backup.

## Open innovation

The séance can use open-weight models that run on the user's own machine. That avoids a hosted AI account and request fees, keeps intimate stories out of a third-party inference service, and lets the operator change the model and the visible prompt. The deterministic oracle keeps the terminal usable with the network and model unavailable. Open models make the voice adjustable; the local architecture keeps the personal material close.

## Built with

- HTML, CSS, and vanilla JavaScript with a responsive candlelit terminal and altar.
- IndexedDB for local stories, photos, and offerings; a service worker caches the app shell.
- Python's standard library for a loopback-only web server and Ollama proxy.
- Ollama-compatible open-weight models such as Gemma or Llama.

## License

MIT. See [LICENSE](LICENSE).
