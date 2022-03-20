
░█████╗░░█████╗░████████╗░█████╗░████████╗███████╗███╗░░██╗██╗░██████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝████╗░██║██║██╔════╝
██║░░╚═╝██║░░██║░░░██║░░░███████║░░░██║░░░█████╗░░██╔██╗██║██║╚█████╗░
██║░░██╗██║░░██║░░░██║░░░██╔══██║░░░██║░░░██╔══╝░░██║╚████║██║░╚═══██╗
╚█████╔╝╚█████╔╝░░░██║░░░██║░░██║░░░██║░░░███████╗██║░╚███║██║██████╔╝
░╚════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═╝╚═════╝░


--------------------------------------------------------------------------

# Web crawler

url: [https://www.lojakings.com.br/](https://www.lojakings.com.br/)

# 1. Configuration
Before you run this project and for the proper running of this program you need to set up some variables inside `kings/kings/settings.py`.

## 1.1 SENTRY
This project utilizes [SENTRY](https://sentry.io/) for error tracking.

- `SPIDERMON_SENTRY_DSN`
- `SPIDERMON_SENTRY_PROJECT_NAME`
- `SPIDERMON_SENTRY_ENVIRONMENT_TYPE`

## 1.2 GOOGLE CLOUD PLATFORM

- `GCS_PROJECT_ID` 
- `GCP_CREDENTIALS`
- `GCP_STORAGE`
- `GCP_STORAGE_CRAWLER_STATS`
- `IMAGES_STORE`

## 1.3 DISCORD
- `DISCORD_WEBHOOK_URL`
- `DISCORD_THUMBNAIL_URL`
- `SPIDERMON_DISCORD_WEBHOOK_URL`


# 2. Implemented Brands
- kings-adidas-male [`AdidasMaleSpider`]
- kings-adidas-female [`AdidasFemaleSpider`]
- kings-nike-male [`NikeMaleSpider`]
- kings-nike-female [`NikeFemaleSpider`]

# 3. Build

```shell
cd kings
make docker-build-production
```

# 4. Publish

```shell
make docker-publish-production
```

# 5. Use
- The parameter `brand` could receive one of the following values: [`kings-adidas-male`, `kings-adidas-female`, `kings-nike-male`, `kings-nike-female`].

```shell
docker run --shm-size="2g" gcr.io/cotatenis/cotatenis-crawl-kings:0.4.0 --brand=kings-adidas-male
```
