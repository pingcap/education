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

## Task 2: Connect to TiDB Cloud (5 minutes)
1. On the TiDB Cloud console, click **PingExpressDB**.
2. In the upper right of the pane, click **Connect**. The **Connect to TiDB** dialog displays.
3. Create the traffic filter for the cluster.
   - Click **Allow Access from Anywhere** in Step 1.
   - Click **Create Filter**.
  Note: For production environments, do not enable **Allow Access from Anywhere**.
4. Note the information between the -h and -P parameters; you'll need this for a later step, as you will use it at a later step. For example:  *mysql -u root -h tidb.xxx.xxxxx.us-west-2.prod.aws.tidbcloud.com -P 4000 -p*
5. Click the **Web SQL Shell** tab. 
6. Click **Open SQL Shell** and enter the password for the cluster. You are now able to write SQL commands.

## Task 3: Import the sample data (10 minutes)
Write SQL commands in Web SQL Shell.
1. Create a database.
   ~~~
   CREATE DATABASE PingExpressDB;
   ~~~
2. Create a user of the database. The user name is *'PingExpress_client'*, and you should set your own password to replace *'\<pwd\>'*, such as *'123'*.
   ~~~   
   CREATE USER 'PingExpress_client' IDENTIFIED BY '<pwd>';
   ~~~
3. Grant all privileges to the user you just created.
   ~~~
   GRANT ALL PRIVILEGES ON PingExpressDB.* TO 'PingExpress_client';
   ~~~
4. Navigate to the TiDB Cloud Clusters page and find your dev cluster.
5. In the upper right corner of the pane, click **Import**. The **Data Import Task** page is displayed.
6. Enter the following information, and click **Import** to import the sample data: 	
   - Data Source Type: Select **AWS S3**
   - Bucket URL: 
      ~~~
      s3://pingexpress/data_workshop/
      ~~~
   - Bucket Region: **Asia Pacific (Singapore)**
   - Data Format: **Select TiDB Dumpling**
   - Setup the following credentials for Role ARN: 
      ~~~
      arn:aws:iam::385595570414:role/pingexpress_workshop
      ~~~
   - Target Database:
      - Username: root.
      - Password: Enter your root password.
   - DB/Tables Filter: Leave this field blank.
The data import process takes about 5 minutes. When the data import progress bar shows Success, you have successfully imported the sample data and the database schema in your database. 
Warning: Do not manipulate the data until the importing process finishes. Otherwise, the importing process fails.
7. Check the imported data.
Open Web SQL Shell and enter the cluster password. (Hint: On the TiDB Cloud console, in the upper right of the pane, click Connect, then click the Web SQL Shell tab.)
   - Switch to PingExpressDB. 
      ~~~
      USE PingExpressDB;
      ~~~
   - Check the number of records 
      ~~~
      SELECT COUNT(*) FROM packages;
      ~~~
The result should be 762000.

8. Create TiFlash replicas for the table packages.
   ~~~
   ALTER TABLE packages SET TiFlash REPLICA 1;
   ~~~
   Wait for a few minutes and then run the following query to check whether the TiFlash node is ready.
   ~~~
   SELECT * FROM information_schema.TIFLASH_REPLICA;
   ~~~
   When the TiFlash node is ready, the values of the “AVAILABLE” and “PROGRESS” columns turn to 1.

## Task 4: Connect to TiDB Cloud via Metabase (10 minutes)
In this section, we walk you through the process of connecting to TiDB Cloud via Metabase. For more information, see [How to Connect TiDB Cloud to Metabase](https://en.pingcap.com/blog/how-to-connect-tidb-cloud-to-metabase).

1. Start the Metabase application and click **Let’s get started**.
2. Select your preferred language and click **Next**. 
3. Enter your information and account details in Step 2 and click **Next**.
4. In the **Add your data** step, click the **Database type** drop down menu and select **MySQL**.
5. Specify the following settings
   - Name: PingExpressDB
   - Host: <your_tidb_cloud_ip_address_obtained_previously>.
   - Port: 4000
   - Database name: PingExpressDB
   - Username: root
   - Password: <password_of_your_tidb_cluster>
6. Scroll down to the bottom and click Next.
7. For the Usage data preference step, change your preference if needed and click **Next**. 
8. Click **Take me to Metabase**.

## Task 5: Build your dashboards in Metabase (10 minutes)
1. Create a dashboard.
   In the top right corner of the dashboard, click the **+** sign, and then choose **New Dashboard**. 
   1. Enter the name as *PingExpress_dashboard*.
   2. Click **Create**.
   3. Click **Save**.
2. Add a question.
   1. In the top right corner of the dashboard, click the **+** sign, and then choose **SQL Query**.
   2. Select **PingExpressDB** as the database. 
   3. Find the number of packages in processing. Enter the following query:
      ~~~
      SELECT courier, count(*) AS numPackages
      FROM packages
      WHERE transaction_kind != "4_pkg_out"
      GROUP BY courier
      ORDER BY count(*) DESC;
      ~~~
      Click Run
   4. After getting the result, click the **Visualization** button, and then choose **Table**.
   5. Click Conditional Formatting.
      - Click **Add a rule**
      - Choose **numPackages**
   6. In **When a cell in this column…** choose **is greater than**
   7. Enter number *150,000*
   8. Choose your favorite background color.
3. Save the question.
   1. In the upper right corner, click Save.
   2. Enter the name *Number of Packages in Processing*. 
   3. When being asked if you would like to add this question to the dashboard, click **Yes please!**, and choose **PingExpress_dashboard**. 
   4. The result will now appear on the dashboard.
   5. Click Save. 
4. Navigate to the clock button on the upper right corner, and set auto-refresh as 1 minute.

## Task 6: Execute the program (10 minutes)
1. Clone the program to your local machine, or any virtual machines provided by your cloud vendor.
   ~~~
   git clone https://github.com/pingcap/education.git
   ~~~
2. Go to the directory for **PingExpress_DemoCorp**.
   ~~~
   cd education/PingExpress_DemoCorp
   ~~~
3. Update the connection string in the main method of PingExpress_client_workshop.py. The connection string is in the format:
   ~~~
   tidb://<client_name>:<pwd>@xxx.xxxx.xxxx.xxxx.prod.aws.tidbcloud.com:4000/<DB_name>
   ~~~
   For example, if the client name is PingExpress_client,  the password is 123, and the database name is PingExpressDB,, the connection string is:
   ~~~
   tidb://PingExpress_client:123@xxx.xxxx.xxxx.xxxx.prod.aws.tidbcloud.com:4000/PingExpressDB
   ~~~
4. You can find the host address for TiDB Cloud in Connect to TiDB - Standard Connection - Step 2 in the TiDB Console, in the format: *xxx.xxxx.xxxx.xxxx.prod.aws.tidbcloud.com.*  

5. Execute the program. Enter
   ~~~
   python3 PingExpress_client_workshop.py --execute --clients 50 --duration 200
   ~~~
   The command assumes there will be 50 clients, and the program runs for 200 seconds. 
Note: For TiDB Cloud Developer Tier, the maximum number of connections allowed is 50.

6. Observe the results. When the program starts running, you can navigate to the Metabase dashboard and observe the dashboard being updated in real time.

   ![result](img/result.png)
