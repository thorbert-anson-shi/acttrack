# acttrack

A simple activity tracker built on [FastAPI](https://fastapi.tiangolo.com/) and
[TinyFlux](https://tinyflux.readthedocs.io/en/latest/intro.html)

---

## What `acttrack` does

Keeps a time-series database of activities with the following information:

1. Time at which activity was recorded
2. Hours spent on the activity
3. Either:
   1. A short description of the activity, or
   2. A notable event that took place

I made this because I'd like to keep a simple diary of the things I'm doing.
This is a work in progress, and I am very open to suggestions.

## Notable features

Because `acttrack` uses
[TinyFlux](https://tinyflux.readthedocs.io/en/latest/intro.html) as a
time-series database, all data is stored in a single CSV file. This allows for
simple data backups and migration

## Usage

You can either run the underlying FastAPI application on `uv`, build and run the
OCI image yourself, or use the pre-built `acttrack` image.

### Running the FastAPI application

#### Preparing the environment

The application runs in a `uv`-managed environment. Install the required
dependencies with the following command:

```bash
uv sync --frozen
```

The FastAPI application reads the shell environment and any .env files for the
following variables:

1. `TZ_ZONEINFO`: The human-readable name for the desired IANA timezone (i.e.
   Asia/Bangkok).

You can refer to the
[list of valid timezone names](https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab)
for more information.

It's easiest to set the environment variables in a `.env` file:

```plaintext
TZ_ZONEINFO=Asia/Bangkok
```

#### Running the application

I chose Granian as the Python web server used to run the application. You can
start the Granian server with the following command:

```bash
uv run granian --interface asgi --host 0.0.0.0 --port 8000 main:app
```

### Using the pre-built container image

The container image defaults to serving the application on port 8000. Use the
Docker or Podman port forwarding features to expose the application on a
different port.

To persist activity data, make sure to create a volume mount from your CSV file
to the in-container /app/db.csv file. For example,

```bash
# Now ./db.csv on the host device is mounted to the container
podman run -p 8000:8000 -v ./db.csv:/app/db.csv tbcr.tobtoby.net/acttrack:v1.0
```

#### Podman

```bash
# Authenticate with tbcr.tobtoby.net
podman login tbcr.tobtoby.net

# Pull the acttrack OCI container image
podman pull tbcr.tobtoby.net/acttrack:v1.0

# Run the container
podman run -p 8000:8000 tbcr.tobtoby.net/acttrack:v1.0
```

#### Docker

```bash
# Authenticate with tbcr.tobtoby.net
docker login tbcr.tobtoby.net

# Pull the acttrack OCI container image
docker pull tbcr.tobtoby.net/acttrack:v1.0

# Run the container
docker run -p 8000:8000 tbcr.tobtoby.net/acttrack:v1.0
```
