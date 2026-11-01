# Archived: TiDB education and workshop materials (2021–2022)

This repository is **archived and no longer maintained**. It holds course files and workshop guides that PingCAP used for TiDB training in 2021–2022. It is kept only for historical reference.

**Do not use anything here in production, or as a security example.** The material was written for short-lived classroom clusters. On purpose, it uses settings that are unsafe anywhere else:

- `root` with an empty or example password
- network access open to `0.0.0.0/0`
- `ALL PRIVILEGES` grants
- no TLS
- unpinned build and setup dependencies

The workshops target TiDB Cloud Developer Tier, which no longer exists, so the steps will not work as written.

For current material:

- Hands-on labs: https://labs.tidb.io
- Documentation: https://docs.pingcap.com
- TiDB Cloud: https://docs.pingcap.com/tidbcloud/

## Contents

| Folder | What it was |
|---|---|
| `pingcap101/` | Lab files for the TiDB 101 course (sample data, TiDB Lightning and TiUP configs) |
| `pingcap201/` | Lab files for the TiDB 201 course (DM, TiCDC and eksctl configs, Java samples) |
| `PingExpress_DemoCorp/` | Workshop: a data-intensive app on TiDB Cloud with Metabase |
| `nft_insight/` | Workshop: an NFT analytics app on TiDB Cloud with Retool |
