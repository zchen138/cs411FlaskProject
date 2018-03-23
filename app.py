from flask import Flask
from flask import request, redirect, render_template, url_for
import MySQLdb

app = Flask(__name__)
conn = MySQLdb.connect(host="localhost", user="root", password="pass", db=)