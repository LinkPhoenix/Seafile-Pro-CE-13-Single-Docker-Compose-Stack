# ☁️ Seafile Pro 13 🐳 Single Docker Compose Stack

A production-ready **Seafile Professional Edition 13** deployment using a **single `docker-compose.yml`**, behind **Traefik** (not Caddy) with **Cloudflare** for TLS and DNS.

Good, complete Seafile configurations are hard to find. This repo provides one unified stack (server, SeaDoc, notification, metadata, thumbnail) so you can get running without piecing together multiple compose files or outdated docs.

**📚 Official resources**

- [Official forum](https://forum.seafile.com/) — Community support and discussions  
- [Official setup documentation](https://manual.seafile.com/latest/setup/overview/) — Installation and configuration overview  
- [Extensions (e.g. SeaDoc)](https://manual.seafile.com/latest/extension/setup_seadoc/) — Extra components and online editing

---

## 🔧 Tech stack

| Component | Role |
|-----------|------|
| 🗂️ **Seafile Pro 13** | File sync & share, Seahub, fileserver |
| 🔀 **Traefik** | Reverse proxy, TLS termination, routing |
| ☁️ **Cloudflare** | DNS (ACME challenge), optional CDN/WAF |
| 🗄️ **MariaDB** | Databases (ccnet, seafile, seahub) |
| ⚡ **Redis** | Cache / sessions |
| 📝 **SeaDoc** | Online editing (sdoc) |
| 🔔 **Notification server** | Real-time notifications |
| 📊 **Metadata server** | File metadata / indexing (no Elasticsearch in this setup) |
| 🖼️ **Thumbnail server** | Image thumbnails |

**Current scope (no extra services in this config):**

- ❌ No **Elasticsearch** (full-text search is disabled; SeaSearch can be added later).
- ❌ No **ClamAV** (virus scanning is disabled).

---

## 📁 Project structure

```
.
├── docker-compose.yml      # Single compose: db, redis, seafile, seadoc, notification, md, thumbnail
├── .env.example            # Template for environment variables (copy to .env)
├── conf/                   # Seafile configs to apply after first run
│   ├── gunicorn.conf.py
│   ├── seafdav.conf
│   ├── seafevents.conf
│   ├── seafile.conf
│   └── seahub_settings.py
├── traefik/                # Traefik configuration (certificates, TLS, providers)
│   ├── Traefik.yml
│   └── dynamic/
│       ├── security.yml
│       └── tls.yml
└── original_docker_compose/ # Reference compose fragments this stack was based on
    ├── 00-seafile-server.yml
    ├── 01-seadoc.yml
    ├── 02-notification-server.yml
    ├── 03-metadata-server.yml
    ├── 04-thumbnail-server.yml
    ├── 05-seafile-ai.yml
    ├── 06-collabora.yml
    └── 07-litllm.yml
```

- 📂 **`conf/`** — Copy (or mount) these into your Seafile data directory after the first startup so email, WebDAV, 2FA, and other options match your environment.
- 🔐 **`traefik/`** — Example Traefik setup; adapt to your own Traefik instance and Cloudflare (or other DNS) if needed.
- 📜 **`original_docker_compose/`** — Original per-service compose files used as reference; this repo uses one merged `docker-compose.yml` instead.

---

## ✅ Prerequisites

- 🐋 Docker and Docker Compose
- 🔀 A running **Traefik** instance on a network named `traefik-net` (or adjust `docker-compose.yml` to your network). This stack uses **Traefik** as the reverse proxy, not Caddy.
- ☁️ **Cloudflare** (or another DNS provider) for your domain, if using the provided TLS/ACME setup
- 📜 Seafile Pro license (*ONLY if required by your use case*)

**Hardware (official Seafile Pro recommendations):** 4 cores, 4 GB RAM. For **personal use** without Elasticsearch, you can often run with less; adjust to your load. Personally, for personal use, I have a 4vcore and 8GB at Hetzner with lots of other Docker stacks.

---

## 🚀 Usage

### 1️⃣ Configure environment variables

- Copy the example env file:
  ```bash
  cp .env.example .env
  ```
- Edit **`.env`** according to your setup:
  - **`SUB_DOMAIN`** — Your sub domain (e.g. seafile)
  - **`SEAFILE_SERVER_HOSTNAME`** — Your public hostname (e.g. `$SUB_DOMAIN.example.com`).
  - **`JWT_PRIVATE_KEY`** — Generate a secret, e.g. `openssl rand -hex 32`.
  - **Database and Redis** — Set `SEAFILE_MYSQL_DB_PASSWORD`, `REDIS_PASSWORD`, `INIT_SEAFILE_MYSQL_ROOT_PASSWORD`, `INIT_SEAFILE_ADMIN_EMAIL`, `INIT_SEAFILE_ADMIN_PASSWORD` (and any other required vars).
  - **Email** — If you use Seahub email, set `EMAIL_HOST_PASSWORD` (and ensure `conf/seahub_settings.py` matches your SMTP host/user).

### 2️⃣ Configure Traefik

- This repo includes an example Traefik configuration in **`traefik/`** (static config + dynamic TLS/security).
- Ensure your Traefik instance:
  - Uses the same certificate resolver and entrypoint names referenced in the Seafile service labels (e.g. `certresolver=cloudflare`, `entrypoints=websecure`).
  - Is on the **`traefik-net`** network so the Seafile stack can be discovered.
- Adjust **`traefik/Traefik-server-conf.yml`** and **`traefik/dynamic/`** to match your setup (domain, email for ACME, Cloudflare API if using DNS challenge).

### 3️⃣ First launch

- Start the stack:
  ```bash
  docker compose up -d
  ```
- ⏳ Wait for services to become healthy (especially `seafile` and `db`).
- On first run, Seafile will create its data under the volume defined by `SEAFILE_VOLUME` (e.g. `/opt/seafile-pro-13/data`).

### 4️⃣ Apply configuration from `conf/`

- After the first successful start, the Seafile data directory will contain a `conf` (or similar) path where the application reads its config.
- Copy (or bind-mount) the contents of this repo’s **`conf/`** into that directory so that:
  - **`seahub_settings.py`** — Email, ALLOWED_HOSTS, CSRF, WebDAV secret, 2FA, etc.
  - **`seafile.conf`** — Fileserver options.
  - **`seafevents.conf`** — Events, statistics, file history (no Elasticsearch in this example).
  - **`seafdav.conf`** — WebDAV enable/disable and port.
  - **`gunicorn.conf.py`** — Gunicorn settings for Seahub.
- Exact target path depends on your volume layout (e.g. `$SEAFILE_VOLUME/seafile/conf`). See [Seafile Docker docs](https://manual.seafile.com/13.0/setup/setup_ce_by_docker/) for your image’s layout.
- Restart the Seafile container (or the whole stack) after updating config:
  ```bash
  docker compose restart seafile
  ```

### 5️⃣ Access and admin

- 🌐 Open `https://<SEAFILE_SERVER_HOSTNAME>` in a browser.
- Log in with **`INIT_SEAFILE_ADMIN_EMAIL`** / **`INIT_SEAFILE_ADMIN_PASSWORD`** (only valid if set before first run).
- Configure System Admin → Settings as needed; many options are overridden by `conf/seahub_settings.py`.

**Managing the stack** — We recommend [Portainer](https://www.portainer.io/) to manage this stack (start/stop, logs, updates). You can also use the Docker CLI or any other tool you prefer.

---

## 🛠️ Suggested services (optional)

These are suggestions only; other providers and tools work fine.

| Need | Suggestion | Alternatives |
|------|------------|--------------|
| **Mail (no Gmail/Outlook/Yahoo)** | [Stalwart](https://stalw.art/) mail server | More options: [selfh.st — Email](https://selfh.st/apps/?tag=Email) |
| **S3 storage (personal, moderate size)** | [Contabo](https://contabo.com/en-us/object-storage/), [Hetzner](https://www.hetzner.com/), [Backblaze B2](https://www.backblaze.com/b2/) | RIP [Tebi](https://tebi.io/). For larger needs: [European object storage providers](https://european-alternatives.eu/category/object-storage-providers) |
| **VPS** | [Hetzner](https://www.hetzner.com/), [Racknerd](https://my.racknerd.com/aff.php?aff=18277) (*affiliate link*) | [Contabo](https://contabo.com/) (very slow and not very reliable support; use at your own discretion) |

---

## 🤝 Contributing

Contributions are welcome.

- **Pull requests** — Fixes, clearer docs, or safer defaults are appreciated.
- **Configuration variants** — If you have an alternative setup (e.g. with Collabora, SeaSearch, or different storage), consider contributing it as a **variant file** (e.g. `docker-compose.collabora.yml`, `docker-compose.seasearch.yml`) rather than replacing the main `docker-compose.yml`, so others can choose the flavour they need.


---

## 📌 To-Do

- [ ] Improve the usage process in this README (step-by-step, optional checks).
- [ ] Add ClamAV for virus scanning (optional service + config).
- [ ] Add Elasticsearch for full-text search.
- [ ] Provide a script to adjust configuration (e.g. enable/disable WebDAV, SeaDoc, notification) based on user choices.
- [ ] Add configuration variant for **Seafile Community Edition (CE) 13** and more.
