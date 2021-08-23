# Online Example
https://twitternow.ml

username: test1

password: def12345

# Development Environment
`Vagrant` + `VirtualBox` + `PyCharm` + `Ubuntu 18.04`

## Pre-requisite
### 1. Install VirtualBox

https://www.virtualbox.org/wiki/Downloads

### 2. Install Vagrant

 https://www.vagrantup.com/downloads

After installation,
```
$ vagrant --version
Vagrant 2.2.15
```

### 3. Create Virtual Machine

#### 3.1 Preparing Box image

##### 3.1.1 Downloading
https://app.vagrantup.com/hashicorp/boxes/bionic64

Choosing `virtualbox Hosted by Vagrant Cloud (494 MB)`

Renaming downloaded image to `bionic64.box`, and then moving it to the project directory.

##### 3.1.2 Adding Box image
In the current project directory,
```
$ vagrant box add hashicorp/bionic64 bionic64.box
```
hashicorp/bionic64 is the name we gave to Box, hashicorp is the name of the company that developed the Vagrant product, 
and bionic64.box is the path where the Box files are located.

After adding, we can verify via
```
$ vagrant box list
```

#### 3.2 Pre-boot configuration of the virtual machine
##### 3.2.1 Vagrantfile
Renaming `Vagrantfile.tmp` to `Vagrantfile`.

##### 3.2.2 provision.sh

##### 3.2.3 requirements.txt

####3.3 Start the virtual machine
Start the virtual machine:
```
$ vagrant up
```

Log into the virtual machine:
```
$ vagrant ssh
```

Check whether vagrant up worked properly
```
$ python --version

$ python -m django --version
```

### 4. post-boot configuration of the virtual machine
#### 4.1 Allow remote login
```
$ sudo vim /etc/ssh/sshd_config
```
Set the `force_color_prompt` option in the file to `yes` and remove the preceding comment

#### 4.2 Remote login
The IP of the virtual machine is the private IP `192.168.33.10` we set up earlier, and the username and password are by default is `vagrant`

```
$ cd /vagrant
```

#### 4.3 Install proxy plugin
In order to let virtual machine use proxy, we need to install vagrant-proxyconf.
```
$ vagrant plugin install vagrant-proxyconf
```

#### 4.4 Download Google Cloud Credential.json
Creat Owner of the Google Cloud project according to:
https://cloud.google.com/docs/authentication/getting-started

and get the json file, rename it to `credential.json` and move it to the project directory.

#### 4.5 Install Memcached
```
$ apt-get install memcached
$ pip install python-memcached
```

#### 4.6 Install Redis
```
$ sudo apt-get install redis
$ pip install redis
```

#### 4.7 Install HBase
##### 4.7.1 Install JDK

https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html

Install `jdk-8u301-linux-x64.tar.gz`

```
sudo mkdir /usr/lib/jvm
sudo tar -zxvf jdk-8u301-linux-x64.tar.gz -C /usr/lib/jvm
```

Modify the environment variable.
```
vi ~/.bashrc
```

Append the following contents.
```
#set oracle jdk environment
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_301 ## Note: this directory should be replaced with decompressed directory.
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
```

Let the environmental variables be valid.
```
source ~/.bashrc
```

Check the installed Java environment.
```
java -version
# java version "1.8.0_281"
# Java(TM) SE Runtime Environment (build 1.8.0_281-b09)
# Java HotSpot(TM) 64-Bit Server VM (build 25.281-b09, mixed mode)
javac -version
# javac 1.8.0_281
```

#### 4.7.2 Download HBase
https://www.apache.org/dyn/closer.lua/hbase/

```
$ tar xzvf hbase-2.4.5-bin.tar.gz
$ cd hbase-2.4.5
```

Setting `JAVA_HOME` in `conf/hbase-env.sh`  
```
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_301
```

Modify `conf/hbase-site.xml`
```
<configuration>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>false</value>
  </property>
  <property>
    <name>hbase.tmp.dir</name>
    <value>./tmp</value>
  </property>
  <property>
    <name>hbase.rootdir</name>
    <value>file:///home/vagrant/hbase</value>
  </property>
  <property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/home/vagrant/zookeeper</value>
  </property>
  <property>
    <name>hbase.unsafe.stream.capability.enforce</name>
    <value>false</value>
    <description>
      Controls whether HBase will check for stream capabilities (hflush/hsync)

      Disable this if you intend to run on LocalFileSystem, denoted by a rootdir

      with the 'file://' scheme, but the midndful of the NOTE below.

      WARNING: Setting this to false blinds you to potential data loss and
      inconsistent system state in the event of process and/or node failures.
      If HBase is complaining of an inability to use hsync or hflush its most
      likely not a false positive.
    </description>
  </property>
</configuration>
```

Start HBase.
```
bash bin/start-hbase.sh
```

Visit `http://192.168..33.10:16010` to check HBase status.

HBase command line:
```
$ ./bin/hbase shell
hbase(main):001:0>
```

### 4.8 Thrift

#### 4.8.1 Download thrift
https://thrift.apache.org/download.html

#### 4.8.1 Install dependencies
```
$ sudo apt-get install automake bison flex g++ git libboost-all-dev libevent-dev libssl-dev libtool make pkg-config
```

If dependencies installing failed, please modify the Ubuntu sources
```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo vi /etc/apt/sources.list
```

Change the `sources.list` into 
```
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe
multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe
multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted
universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted
universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted
universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted
universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted
universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted
universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted
universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted
universe multiverse
```

Update sources
```
sudo apt-get update
```

#### 4.8.2 Build and install
```
tar zxf thrift-0.14.2.tar.gz
cd thrift-0.14.2
./configure
make
make install
```

If encounter following error during `configure`:

`configure: error: cannot run C compiled programs`

Maybe you use AMD CPU. Please run the following command:
```
git clone https://github.com/apache/thrift.git
cd thrift
git checkout remotes/origin/0.14.2
./bootstrap.sh
./configure
make
sudo make install
```


#### 4.8.3 Start Thrift service of HBase
```
$ bin/hbase-daemon.sh start thrift
```

#### 4.8.4 Install happybase
```
pip install happybase
```

#### 4.8.5 Verification
```
import happybase
conn = happybase.Connection("192.168.33.10")
families = {'cf1': dict()}
print(conn.tables())
conn.create_table('mytable', families)
print(conn.tables())
```

### 4.9 Create Database tables
```
python manage.py makemigrations
python manage.py test
python manage.py migrate
```

### 4.10 Create superuser
```
vagrant@vagrant:/vagrant$ python manage.py shell
Python 3.6.9 (default, Jan 26 2021, 15:33:00)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.contrib.auth.models import User;
>>> username='admin'
>>> password='admin'
>>> email='admin@twitter.com'
>>> if not User.objects.filter(username=username).exists():
...   User.objects.create_superuser(username, email, password)
...   print('Superuser created.')
... else:
...   print('Superuser creation skipped.')
...
<User: admin>
Superuser created.
>>>
```

### 4.11 Check

Visit `http://localhost/admin`

Username: Admin

Password: Admin


## 5. Development environment configuration
File->Settings-> search "python interpreter",

Click the `gear mark`.

Select `add`.

Choose `Vagrant`

Click `OK`, 'OK'


Run->Edit Configurations
Click `+`(Add New Configuration)
Choose `Django Server` (If the environment already have a Django Server Configuration, we don't need to add anymore)

In the Configuration,

Host: `0.0.0.0`

Maybe we need to fix Django dependencies.

Just click `fix` button.

Choose `Enable Django Support`.
Then set the project root and the path of `settings.py`
Click Ok.

Then we can run on Pycharm.


### Appendix
#### Fanout NewsFeeds
```
- tweets
tweets.api.views.py
  create():
    NewsFeedService.fanout_to_followers(tweet)
  
  1 tweet对应多个 新鲜事，发推人的本身的时间线，关注发推人的时间线
  fanout_newsfeeds_main_task.delay(tweet.id, tweet.timestamp, tweet.user_id)
    @shared_task() # 用 celery 的 decorator，将下面的函数放到 celery 的队列中，进行异步的 fanout
      获取 HBase 中的 followers 列表
      fanout_newsfeeds_batch_task(tweet_id, created_at, follower_ids)
        newsfeeds = NewsFeedService.batch_create(batch_params)
        HBase
          HBaseNewsFeed.batch_create() # hbase row_key = ('user_id', 'created_at')
        Redis
          push_newsfeed_to_cache() 
    NewsFeed.objects.create()
    把 newsfeeds 放到 redis 里，这样就存储到了磁盘里
    RedisHelper.push_object(key, newsfeed, lazy_load_newsfeeds)
      # 函数里是 redis 有的就直接返回，否则，用HBaseNewsFeed.filter() 获取 HBase 里的 newsfeeds，并将其放入到 Redis里
```

#### NoSQL
```
 Friendships: 保存到了 HBase 里。
 NewsFeeds: 保存到了 HBase 和 Redis 里。
 Tweets: 将整个 Tweets 表保存到 Redis里。
 UserProfile: 保存到了 Memcached 里。
```

### Denormalization
```
comments: likes. listener，在 Model 里定义 incr_comments_count 和 decr_comments_count
同时，会更新数据库和 redis 里的应用

Tweets 只是增加了 likes_counts 和 comments_counts，并没有像 comments 一样定义函数来增加减少 counts。
```
