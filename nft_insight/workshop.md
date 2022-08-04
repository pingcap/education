# Workshop sheet: Building a Crypto Analytics Application with TiDB Cloud & Retool
In this workshop, we will build an NFT Insight application with TiDB cloud and Retool. 

## Task 1: Create a TiDB Developer Tier cluster (10 minutes)
1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up for an account.
2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.
3. Click **Create a Cluster**. 
4. Click **Developer Tier**.
5. On the **Create a Cluster** page, set up **Cluster Name**. (In this tutorial, we will call our cluster **nftInsight**).
6. Choose a **US-West-2 (Oregon)** as your **Region**. 
7. Click **Create**.
8. Enter your **Root Password**.
9. Add **0.0.0.0/0** to IP Access List by clicking **Allow Access from Anywhere**. (Note: In production environment, do not use Allow Access from Anywhere)
10. Click Apply.

Your TiDB Cloud cluster will be created in approximately 5 to 10 minutes.

## Task 2: Import the sample data (15 minutes)
Write SQL commands in your terminal.
1. Click your cluster **NFTInsight**.

2. Click **Connect**, the Connect to TiDB panel shows.

3. Click the **Web SQL Shell** tab.

4. Click **>_ Open SQL Shell**.

5. Enter the root password.

6. Create a user of the database. The user name is *'<your_tanent_id>_client'*, and you should set your own password to replace *'\<pwd\>'*, such as *'123'*.
   ~~~   
   CREATE USER '<your_tanent_id>.client' IDENTIFIED BY '<pwd>';
   ~~~
7. Grant all privileges to the user you just created.
   ~~~
   GRANT ALL PRIVILEGES ON nft.* TO '<your_tanent_id>.client';
   ~~~
   
8. Create a database.
   ~~~
   CREATE DATABASE nft;
   ~~~

9. Switch to the database just created.
   ~~~
   use nft;
   ~~~

10. Create 3 tables.
   ~~~
   CREATE TABLE assets (
      asset_id BIGINT PRIMARY KEY,
      asset_name TEXT,
      collection_slug VARCHAR(254),
      asset_contract_date TIMESTAMP,
      owner_id BIGINT,
      asset_url TEXT,
      asset_img_url TEXT
   );

   CREATE TABLE collections (
      collection_slug VARCHAR(254) PRIMARY KEY,
      collection_name TEXT,
      collection_url TEXT
   );

   CREATE TABLE events (
      event_id BIGINT PRIMARY KEY,
      event_time TIMESTAMP,
      asset_id BIGINT, 
      collection_slug VARCHAR(254),
      event_auction_type TEXT,
      event_contract_address TEXT,
      event_quantity INT,
      event_payment_symbol TEXT,
      event_total_price DOUBLE
   );
   ~~~

11. Add index to the tables
   ~~~
   CREATE INDEX collection_slug_assets_index ON assets (collection_slug);
   CREATE INDEX collection_slug_events_index ON events (collection_slug);
   CREATE INDEX asset_id_events_index ON events (asset_id);
   ~~~ 

12. Navigate to the TiDB Cloud Clusters page and find your dev cluster.

13. In the upper right corner of the pane, click **Import**. The **Data Import Task** page is displayed.

14. Enter the following information, and click **Import** to import the sample data: 	
   - Data Source Type: Select **AWS S3**
   - Bucket URL: 
      ~~~
      s3://nft-insight-na/nft_insight_workshop/
      ~~~
   - Data Format: **CSV**
   - Setup the following credentials for Role ARN: 
      ~~~
      arn:aws:iam::577523860935:role/nft-insight-workshop-0803
      ~~~
   - CSV Configuration: Leave as default
   - Enter your root password
   - DB/Tables Filter: (Leave Blank)
   - Object Name Pattern: 
      ~~~
      assets.csv
      ~~~
   - Target Table Name: 
      ~~~
      nft.assets
      ~~~
   - Similarly, import table **collections** and **events**.

15. Create TiFlash replicas for all three tables.
   ~~~
   ALTER TABLE assets SET TiFlash REPLICA 1;
   ALTER TABLE collections SET TiFlash REPLICA 1;
   ALTER TABLE events SET TiFlash REPLICA 1;
   ~~~

16. Wait for a few minutes and then run the following queries to check whether the TiFlash node is ready.
   ~~~
   SELECT * FROM information_schema.TIFLASH_REPLICA;
   ~~~
   When the TiFlash node is ready, the values of the “AVAILABLE” and “PROGRESS” columns turn to 1.

## Task 3: Build your NFT insight applications in Retool (15 minutes)
1. (Sign up and) log into your [Retool](https://retool.com/) account.

2. Click the **Resource** tab.

3. Click **Create new** on the upper right corner.

4. Choose **Create a new resource**.

5. Select **MySQL** as the type.

6. Enter your database connection details.
   - Name: NFT-data
   - Folder: &lt;Leave_as_default&gt;
   - Host: &lt;your_tidb_cloud_ip_address&gt;
   - Port: 4000
   - Database name: nft
   - Username: root
   - Password: &lt;password_of_your_tidb_cloud_cluster&gt;
   - Click **Create resource**

7. When prompted, choose **Create an app**

8. Enter **App name**: NFT.

9. Click Create.

10. Enter the query to find how many trades there are everyday.
   ~~~
     SELECT DATE(event_time) AS "DATE", count(*)
       FROM events 
   GROUP BY DATE(event_time) 
   ORDER BY DATE(event_time);
   ~~~

11. On the panel on the right hand side, drag Chart onto the canvas. 

12. You may also try the following queries
   - Enter the following query to find how much ETH currency is traded everyday.   
   ~~~
     SELECT DATE(event_time) AS "Date", SUM(event_total_price) AS "Volume ETH"
       FROM events
      WHERE event_payment_symbol = 'ETH'
   GROUP BY DATE(event_time)
   ORDER BY DATE(event_time);
   ~~~
   - Enter the following query to find what the most expensive assets are in Q1 2022.
   ~~~
       SELECT a.asset_name AS 'NFT', c.collection_name AS 'Collection Name', event_total_price AS 'Price (ETH)', a.asset_url AS 'URL'
         FROM events e
   INNER JOIN collections c ON c.collection_slug = e.collection_slug
   INNER JOIN assets a ON a.asset_id = e.asset_id
        WHERE event_payment_symbol = 'ETH'
          AND event_time between '2022-01-01 00:00:00' and '2022-03-31 23:59:00' 
     ORDER BY event_total_price DESC
        LIMIT 10;
   ~~~
   - Enter the following query to find the top 50 popular collections.
   ~~~
     SELECT collections.collection_slug AS 'Collection Slug', collection_name as 'Collection Name', SUM(event_total_price) as TotalVolumeETH
       FROM events, collections 
      WHERE collections.collection_slug = events.collection_slug
        AND event_payment_symbol = 'ETH'
   GROUP BY collections.collection_slug 
   ORDER BY TotalVolumeETH DESC
      LIMIT 50;
   ~~~



