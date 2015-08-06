djrq Installation instructions.

Installation is easy, only python is required, and virtualenv is strongly recommended. These instructions assume you will be using virtualenv.

You will need to decide where to install DJRQ. A good idea would be: ~/www/djrq

Here are the simple steps to getting DJRQ running in development mode.

brian@cyberman ~ $ mkdir -p ~/www
brian@cyberman ~ $ cd ~/www
brian@cyberman ~/www $ git clone https://github.com/bmillham/djrq.git

DJRQ will now be in ~/www/djrq

Now setup the virtualenv

brian@cyberman ~/www $ cd djrq
brian@cyberman ~/www/djrq $ virtualenv --distribute --no-site-packages .

This installs virtualenv to ~/www/djrq. Now activate the vitrualenv

brian@cyberman ~/www/djrq $ . bin/activate

Now install WebCore and all dependencies

(djrq)brian@cyberman ~/www/djrq $ cd DJRQ
(djrq)brian@cyberman ~/www/djrq/DJRQ $ python setup.py install

Step 2 may take a little while to run, as it's installing dependencies. If installing oursql fails, you will need to install libmysqlclient-dev

DJRQ, WebCore and all dependencies are now installed.
Now, copy development.example.ini to development.ini  (~/www/djrq/DJRQ/development.example.ini)
Edit development.ini, and change the db.djname.url lines (there are 2 of them) to match your database credentials.

At this time, only 1 DJ database is supported, but the example does show more than one. This will work in the near future.

One final step now. DJRQ uses tables in the Ampache database that do not exist in a
normal Ampache database, so you will need to run a script to create those tables.

A warning here, after runing this script, there is a possiblility that you will not
be able to update Ampache to a newer version, as is may not recognize the database as
an Ampache database.

You will still be able to use your existing Ampache to update your database, it just
won't upgrade anymore. (And that's probaby a good thing, as upgrading Ampache may also
break IDJC!)

To run the script, you will need to copy it up one directory:

(djrq)brian@cyberman ~/www/djrq/DJRQ $ cp tools/create-extra-djrq-tables.py .

Edit it for your database credentials. Look for this line:

ampache_engine = create_engine('mysql+oursql://sqlalchemy:password@localhost/ampache1', echo=False, encoding='utf8')

And change the user, password, host and database to match your setup. The syntax is:
mysql+oursql://user:password@host/database

Run the script:
(djrq)brian@cyberman ~/www/djrq/DJRQ $ python create-extra-djrq-tables.py


Now it's time to test things out!

Make sure you still have your virtualenv active.

(djrq)brian@cyberman ~/www/djrq/DJRQ $ paster serve --reload development.ini

Now point your web browser to localhost:8080 to view your site!

Setting up to run under nginX in production mode:
COMING SOON!

nginx sample config file is in nginx.example.conf
