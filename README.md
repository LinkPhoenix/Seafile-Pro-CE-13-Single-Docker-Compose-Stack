# ☁️ Seafile Pro 13 🐳 Single Docker Compose Stack

A production-ready **Seafile Professional Edition 13** deployment using a **single `docker-compose.yml`**, behind **Traefik** (not Caddy) with **Cloudflare** for TLS and DNS.

Good, complete Seafile configurations are hard to find. This repo provides one unified stack (server, SeaDoc, notification, metadata, thumbnail) so you can get running without piecing together multiple compose files or outdated docs.

**📚 Official resources**

- [Official forum](https://forum.seafile.com/) — Community support and discussions  
- [Official setup documentation](https://manual.seafile.com/latest/setup/overview/) — Installation and configuration overview  
- [Extensions (e.g. SeaDoc)](https://manual.seafile.com/latest/extension/setup_seadoc/) — Extra components and online editing

---

## 📑 Index

- [Tech stack](#-tech-stack)
- [Project structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Usage](#-usage)
  - [Configure environment variables](#1️⃣-configure-environment-variables)
  - [Configure Traefik](#2️⃣-configure-traefik)
  - [First launch](#3️⃣-first-launch)
  - [Apply configuration from `conf/`](#4️⃣-apply-configuration-from-conf)
  - [Small VPS (low RAM)](#small-vps-low-ram)
  - [Configure SeaSearch (full-text search)](#configure-seasearch-full-text-search)
  - [Access and admin](#5️⃣-access-and-admin)
- [Suggested services (optional)](#️-suggested-services-optional)
- [Seafile Community Edition 13 (CE) — very lightweight](#-seafile-community-edition-13-ce)
- [Contributing](#-contributing)
- [To-Do](#-to-do)

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
| 📊 **Metadata server** | File metadata / indexing |
| 🖼️ **Thumbnail server** | Image thumbnails |
| 🔍 **SeaSearch** | Full-text search (replaces Elasticsearch) |

**Current scope:**

- ✅ **SeaSearch** is included for full-text search (see [Configure SeaSearch](#configure-seasearch-full-text-search) below).
- ❌ No **ClamAV** (virus scanning is disabled).

---

## 📁 Project structure


- 📂 **`conf/`** — Copy (or mount) these into your Seafile data directory after the first startup so email, WebDAV, 2FA, and other options match your environment.
- 📂 **`conf-CE/`** — Configuration files for **Seafile Community Edition 13** when using `docker-compose-CE.yml` (see [Seafile CE 13](#-seafile-community-edition-13-ce) below).
- 🔐 **`traefik/`** — Example Traefik setup; adapt to your own Traefik instance and Cloudflare (or other DNS) if needed.
- 📜 **`original_docker_compose/`** — Original per-service compose files used as reference; this repo uses one merged `docker-compose.yml` instead.

---

## ✅ Prerequisites

- 🐋 Docker and Docker Compose
- 🔀 A running **Traefik** instance on a network named `traefik-net` (or adjust `docker-compose.yml` to your network). This stack uses **Traefik** as the reverse proxy, not Caddy.
- ☁️ **Cloudflare** (or another DNS provider) for your domain, if using the provided TLS/ACME setup
- 📜 Seafile Pro license (*ONLY if required by your use case*)

**Hardware (official recommendations):**

- **Pro** ([setup pro](https://manual.seafile.com/13.0/setup/setup_pro_by_docker/)): at least **4 GB RAM** and a **4-core CPU** (> 2 GHz).
- **CE** ([setup CE](https://manual.seafile.com/13.0/setup/setup_ce_by_docker/)): at least **2 GB RAM** and a **2-core CPU** (> 2 GHz). See [Seafile CE 13 (CE)](#-seafile-community-edition-13-ce) for the lite stack.

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
- **SeaSearch** — If you use SeaSearch, set the token in `conf/seafevents.conf` and optionally `INIT_SS_ADMIN_USER` / `INIT_SS_ADMIN_PASSWORD` in `.env` (see [Configure SeaSearch](#configure-seasearch-full-text-search)).

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
  - **`seafevents.conf`** — Events, statistics, file history, SeaSearch (indexation).
  - **`seafdav.conf`** — WebDAV enable/disable and port.
  - **`gunicorn.conf.py`** — Gunicorn settings for Seahub.
- Exact target path depends on your volume layout (e.g. `$SEAFILE_VOLUME/seafile/conf`). See [Seafile Docker docs](https://manual.seafile.com/13.0/setup/setup_ce_by_docker/) for your image’s layout.
- Restart the Seafile container (or the whole stack) after updating config:
  ```bash
  docker compose restart seafile
  ```

#### Small VPS (low RAM)

**Tip:** For **personal use** (CE or Pro), you can reduce RAM by tuning the options below—the repo’s `conf/seafile.conf` and `conf-CE/seafile.conf` are already tuned for low memory. **CE** can run with less than the official 2 GB; **Pro** with less than 4 GB (e.g. without Elasticsearch, moderate sync). Some parameters in the table are **Pro only**; on Community Edition, use only `worker_threads` and `fs_cache_limit`, and omit or remove `fs_id_list_max_threads`.

If you run Seafile on a **small VPS** with limited RAM, edit **`conf/seafile.conf`** (Pro) or **`conf-CE/seafile.conf`** (CE) and adjust these options (all under `[fileserver]`). Below are the values used and their **defaults** for reference.

| Option | Default | Edition | Purpose |
|--------|---------|---------|--------|
| `worker_threads` | `10` | CE & Pro | Number of HTTP worker threads. Lower value reduces RAM (e.g. `6`). |
| `fs_cache_limit` | `2000` (2 GB, in MB) | CE & Pro | Go fileserver in-memory fs cache. Reduce (e.g. `500`) on a small VPS. |
| `fs_id_list_max_threads` | `10` | **Pro only** (since 12.0.10) | Max concurrent fs-id-list handlers (sync). Lower (e.g. `5`) to reduce RAM. Omit or remove in Community Edition. |

If you use MySQL in this stack and configure it in `seafile.conf`, you can also set **`max_connections`** in the `[database]` section (default `100`); e.g. `30` or `20` for a small server.

After changing `seafile.conf`, restart the Seafile container so the new values take effect. See [Seafile 13.0 — seafile.conf (Go Fileserver)](https://manual.seafile.com/13.0/config/seafile-conf/#go-fileserver) for full details.

#### Configure SeaSearch (full-text search)

The stack includes **SeaSearch** for full-text search. To get indexing and search working:

1. **SeaSearch credentials in `.env`**

   - **Simple option (same account as Seafile admin)** — In `.env` use:
     ```bash
     INIT_SS_ADMIN_USER=$INIT_SEAFILE_ADMIN_EMAIL
     INIT_SS_ADMIN_PASSWORD=$INIT_SEAFILE_ADMIN_PASSWORD
     ```
     The SeaSearch password will then always match the one set at deployment for the Seafile admin.

   - **Custom option** — Set a dedicated SeaSearch user and password:
     ```bash
     INIT_SS_ADMIN_USER=seasearch-admin@example.com
     INIT_SS_ADMIN_PASSWORD=your_seasearch_password
     ```
     Use **these** values to generate the token (next step).

2. **Generate the auth token**

   The token is **base64** of `username:password` (the same credentials used for SeaSearch in `.env`).

   - On Linux/macOS:
     ```bash
     echo -n "your_email:your_password" | base64
     ```
   - On PowerShell (Windows):
     ```powershell
     [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your_email:your_password"))
     ```
   Use `INIT_SEAFILE_ADMIN_EMAIL:INIT_SEAFILE_ADMIN_PASSWORD` if you chose the simple option, otherwise `INIT_SS_ADMIN_USER:INIT_SS_ADMIN_PASSWORD`.

3. **Configure `conf/seafevents.conf`**

   - Keep **`[INDEX FILES]`** with **`enabled = false`** (this disables the old Elasticsearch-based indexing).
   - In **`[SEASEARCH]`** set **`enabled = true`** and replace `<your auth token>` with the base64 token you generated:
     ```ini
     [INDEX FILES]
     enabled = false

     [SEASEARCH]
     enabled = true
     seasearch_url = http://seasearch:4080
     seasearch_token = <paste_your_base64_token_here>
     interval = 30m
     ```
   Then restart the Seafile container (and seafevents if you run it separately):
   ```bash
   docker compose restart seafile
   ```

4. **Force the first indexing (without waiting 10 minutes)**

   By default, indexing may run on a schedule (e.g. every 10 minutes). To run the **first indexing immediately** in Docker:

   ```bash
   docker exec -it seafile bash
   cd /opt/seafile/seafile-server-latest
   ./pro/pro.py search --update
   exit
   ```

   Once indexing finishes, file search will be available in the interface.

5. **Indexing interval (small or low-usage environments)**

   For low-usage or small setups, it is recommended to **increase** `interval` in `[SEASEARCH]` (and optionally in `[SEAHUB EMAIL]`), e.g. `interval = 30m` or more. The provided `conf/seafevents.conf` already uses `30m` for SeaSearch. For heavier use you can set `10m` for more frequent search updates.

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

## 🐧 Seafile Community Edition 13 (CE)

This repo also provides a **very lightweight** **Community Edition** stack for Seafile 13, based on the [official CE Docker setup](https://manual.seafile.com/13.0/setup/setup_ce_by_docker/). No Pro license required.

**Why “lite”?** Only three services run: **database**, **Redis**, and **Seafile**. There are no extra containers (SeaDoc, notification server, metadata server, thumbnail server, SeaSearch). That means lower RAM/CPU usage and a simpler setup—ideal for a small server or testing.

| Included (CE lite) | Not included |
|--------------------|--------------|
| Seafile server, Seahub, fileserver | SeaDoc (online editing) |
| MariaDB, Redis | Notification server (real-time) |
| WebDAV, 2FA, email, stats, file history | Metadata server |
| Traefik integration | Thumbnail server |
| | SeaSearch (full-text search) |

**Files:**

| File | Purpose |
|------|---------|
| **`docker-compose-CE.yml`** | Compose for CE: `db`, `redis`, `seafile` only. |
| **`.env-ce.example`** | Example environment variables for CE. Copy to `.env-ce` and edit. |
| **`conf-CE/`** | Config files for CE: `seafile.conf`, `seafevents.conf`, `seahub_settings.py`, `gunicorn.conf.py`, `seafdav.conf`. |

**Usage:**

1. Copy the CE env file: `cp .env-ce.example .env-ce`
2. Edit **`.env-ce`**: set `SEAFILE_SERVER_HOSTNAME`, `JWT_PRIVATE_KEY`, `SEAFILE_MYSQL_DB_PASSWORD`, `INIT_SEAFILE_MYSQL_ROOT_PASSWORD`, `INIT_SEAFILE_ADMIN_EMAIL`, `INIT_SEAFILE_ADMIN_PASSWORD`.
3. Start the stack:  
   `docker compose -f docker-compose-CE.yml --env-file .env-ce up -d`
4. After first start, copy (or mount) **`conf-CE/`** into your Seafile data directory (e.g. `SEAFILE_VOLUME/seafile/conf/`) and adjust domain/email in `seahub_settings.py`.

CE uses the image `seafileltd/seafile-mc:13.0-latest` and the network `seafile-ce-net`; Traefik labels use `APP_NAME_CE` (default `seafile-ce`) so you can run CE alongside Pro on the same host with different hostnames.

---

## 🤝 Contributing

Contributions are welcome.

- **Pull requests** — Fixes, clearer docs, or safer defaults are appreciated.
- **Configuration variants** — If you have an alternative setup (e.g. with Collabora, SeaSearch, or different storage), consider contributing it as a **variant file** (e.g. `docker-compose.collabora.yml`, `docker-compose.seasearch.yml`) rather than replacing the main `docker-compose.yml`, so others can choose the flavour they need.


---

## 📌 To-Do

- [ ] Improve the usage process in this README (step-by-step, optional checks).
- [ ] Add ClamAV for virus scanning (optional service + config).
- [ ] Provide a script to adjust configuration (e.g. enable/disable WebDAV, SeaDoc, notification) based on user choices.
- [x] Add configuration variant for **Seafile Community Edition (CE) 13** — see section below.
