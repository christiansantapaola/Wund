import requests
import time
import hashlib
import notify2


class UpdateDaemon:
    """
    UpdateDaemon will check periodically for all the stored website if
    they got updated.
    """
    def __init__(self, db, sleep_time, daemonName):
        self.db = db
        self.sleep_time = sleep_time
        self.daemonName = daemonName
        notify2.init(self.daemonName)
    def run(self):
        """
        run() will start the daemon.
        """
        while True:
            self.check()
            time.sleep(self.sleep_time)

    def check(self):
        """
        check() will check if all the websites inside the database had been updated since the last check.
        """
        websites = self.db.get_websites()
        for website in websites:
            resp = requests.get(website)
            hasher = hashlib.sha256()
            hasher.update(bytes(resp.text, encoding='utf8'))
            newHash = hasher.hexdigest()
            oldHash = self.db.get_hash(website)                
            if oldHash != newHash:
                self.db.update_website_hash(website, newHash)
                self.notify_update(website, oldHash, newHash)

    def notify_update(self, websites, oldHash, newHash):
        """
        notify_update() will notify the system that a website has been update.
        """
        n = notify2.Notification("{} has been modified!".format(websites),
                "{} has been modified!".format(websites))
        n.show()
 
