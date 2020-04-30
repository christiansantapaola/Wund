import sqlite3

class Database:
    """
    Database will talk with the database.
    All the interaction with it, the SQL code and the transaction to disk
    should be here.
    """
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
    def init(self):
        """
        init(): will init the database schema.
        """
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Websites (
                    ID INTEGER PRIMARY KEY,
                    website varchar unique,
                    hash binary(64)
                        );""")
        self.conn.commit()
        self.conn.execute("""CREATE TABLE IF NOT EXISTS History (
                        ID INTEGER PRIMARY KEY,
                    website INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (website)
                        REFERENCES Websites(ID)
                        );""")
        self.conn.commit()
        self.conn.execute("""CREATE TRIGGER IF NOT EXISTS UPDATE_HISTORY
                    BEFORE UPDATE OF hash ON Websites
                    FOR EACH ROW
                    BEGIN
                    INSERT INTO History(website)
                        VALUES (new.ID);
                    END;""")

    def insert_website(self, website):
        """
        insert_website() will insert a new website represented as url like protocol://url.
        Usualy as http[s]://www.domain.com
        """
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO Websites(website) VALUES (?)', (website,))
        self.conn.commit()

    def get_websites(self):
        """
        get_websites() return a list of all websites stored inside the database.
        The list is a list of string like:
        [ 'http://www.domain.com', 'https://www.domain2.com' ]
        """
        cursor = self.conn.cursor()
        res = cursor.execute('SELECT website FROM Websites;')
        collection = res.fetchall()
        result = []
        for item in collection:
            result.append(item[0])
        return result

    def remove_website(self, website):
        """
        remove_website() will remove @website from the database if stored in it.
        """
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM Websites WHERE website=?', (website,))
        self.conn.commit()


    def get_hash(self, website):
        """
        get_hash() will return the hash associated to the current payload
        delivered by a GET request of the website url and stored into the
        database.
        """
        cursor = self.conn.cursor()
        res = cursor.execute("""SELECT hash
        FROM Websites
        WHERE website=?;
        """
        , (website, ))
        r = res.fetchall()
        if len(r) != 0:
            return r[0][0]
        else:
            return None

    def get_websites_with_last_update(self):
        """
        get_websites_with_last_update() will return all the pair 
        [ website, last_update ]
        where last_update is a date calculated by this software.
        """
        cursor = self.conn.cursor()
        res = cursor.execute("""SELECT W.website, H.date
                FROM Websites AS W
                    LEFT JOIN
                    History as H
                    ON W.ID = H.website
                WHERE H.date = (SELECT MAX(Hi.date)
                                FROM Websites AS Wi
                                    JOIN History AS Hi
                                    ON Wi.ID = Hi.website
                                WHERE Hi.website = H.website);""")
        return res.fetchall()

    def update_website_hash(self, website, hashvar):
        """
        update_website_hash() will given a valid website update is hash value.
        """
        cursor = self.conn.cursor()
        cursor.execute('UPDATE Websites SET hash = ? WHERE website = ?;', (hashvar, website))
        self.conn.commit()

    def get_history(self):
        """
        get_history() will return a list containing all the pair 
        [ website, date ]
        where the date is when the website was update in the past.
        """
        cursor = self.conn.cursor()
        res = cursor.execute("""SELECT W.website, H.date
                FROM Websites AS W
                     JOIN
                     History AS H
                     ON W.ID = H.website
                     ORDER BY H.Date DESC;""")
        collection = res.fetchall()
        result = []
        for item in collection:
            result.append(item)
        return result
