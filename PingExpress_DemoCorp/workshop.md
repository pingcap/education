# Workshop sheet: Building a Sample Data-Intensive Application with TiDB Cloud
In this workshop, we will build a data-intensive application with TiDB cloud and Metabase. We will show you how TiDB cloud enables real-time insights.

## Disclaimer
- PingExpress_DemoCorp is a dummy company. It does NOT reflect or imply any real company.
- This workshop  is for demonstration purposes only. Do NOT use any material (including but not limited to code, and commands) from this tutorial in production environments.

## Before You Begin
You should have the following software and packages installed: 
- [Python](https://www.python.org/downloads/) (v. 3+)
- [MySQL connector for Python](https://github.com/mysql/mysql-connector-python)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [sqlalchemy-tidb](https://github.com/pingcap/sqlalchemy-tidb)
- [Metabase](https://www.metabase.com/docs/latest/operations-guide/installing-metabase.html)

Note: It is recommended to use pip3 to install packages, such as SQLAlchemy. We also suggest NOT to use the Mac application version for Metabase. It is gradually being phased out. We recommend you run Metabase on [Heroku](https://www.metabase.com/docs/latest/operations-guide/running-metabase-on-heroku.html). You may also use the jar version for Metabase.

## Task 1: Create a TiDB Developer Tier cluster (10 minutes)
1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.
2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.
3. Click **Create a Cluster**. 
4. Click **Developer Tier**.
5. On the **Create a Cluster (Dev Tier)** page, set up **Cluster Name** and **Root Password**. (In this tutorial, we will call our cluster **PingExpressDB**).
6. Choose a **Region** close to your physical location. 
7. Click **Create**.

Your TiDB Cloud cluster will be created in approximately 5 to 10 minutes.
