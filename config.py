from tools.mail import Mail
from flask_cors import CORS
from flask import Flask, jsonify, request, send_file, abort
import os, json, subprocess, sys, datetime, random, time, re
import constants.const as CONST
import constants.status as STATUS

app = Flask(__name__); 
cors = CORS(app);

PORT = 8080;
IP = "0.0.0.0";
HOST = f"http://localhost:{PORT}";
API_PREFIX = "/api";
SECRET = "abc123";
API_SECRET = "super_secret_api";

mail = Mail("my@gmail.com", "Qwerty123");

db = {};
