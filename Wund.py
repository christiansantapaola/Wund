#!/usr/bin/python3 
import os
import argparse
from database import Database
from daemon import UpdateDaemon

def parse_arguments(parser):
    """
    parse_arguments() will set up the CLI parser arguments and return the parsed arguments.
    """
    parser.add_argument("--database", help="path to the database")
    parser.add_argument("--daemon", help="start the daemon", action="store_true")
    parser.add_argument("--check", help="check for updates", action="store_true")
    parser.add_argument("--init", help="init the database", action="store_true")
    parser.add_argument("--insert", help="insert websites", type=str)
    parser.add_argument("--remove", help="remove websites", type=str)
    parser.add_argument("--list", help="list all websites", action="store_true")
    parser.add_argument("--history", help="list all websites", action="store_true")
    parser.add_argument("--time",
            help="set the value of sleep time in seconds (default 30 min = 60 * 30 seconds)",
            type=int)
    args = parser.parse_args()
    return args

def main():
    # set up environment variable
    HOME = os.path.expanduser("~")
    XDG_CONFIG = HOME + "/.config/"
    APP_NAME = "Wund"
    DATABASE_NAME = "Wund.db"
    DATABASE_PATH = XDG_CONFIG + APP_NAME + "/" + DATABASE_NAME
    parser = argparse.ArgumentParser()
    args = parse_arguments(parser)
    time = 60 * 30
    if len(os.sys.argv) < 2:
        parser.print_help()
    if args.time != None:
        time = args.time
    if args.database:
        db = Database(args.db)
    else:
        if not os.path.exists(XDG_CONFIG + APP_NAME):
            os.makedirs(XDG_CONFIG + APP_NAME)
        if not os.path.exists(DATABASE_PATH):
            db = Database(DATABASE_PATH)
            db.init()
        else:
            db = Database(DATABASE_PATH)
    if args.init:
        db.init()
    if args.insert != None:
        db.insert_website(args.insert)
    if args.remove != None:
        db.remove_website(args.remove)
    if args.list:
        for pair in db.get_websites_with_last_update():
            print("%s %s" % (pair[0], pair[1]))
    if args.history:
        for pair in db.get_history():
            print("%s %s" % (pair[0], pair[1]))
    if args.daemon:
        daemon = UpdateDaemon(db, time, APP_NAME)
        daemon.run()
    if args.check:
        checker = UpdateDaemon(db, time, APP_NAME)
        checker.check()



if __name__ == "__main__":
    main()
