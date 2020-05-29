# Stock REST API 0.1

REST API for Stock Notificator based on Flask micro web framework. 
API feeds the Stock Notificator with links. 
To add, remove, update urls you send post requests.

## Installation 
To run this software you will need:

- python 3

- flask

- flask-restful

- flask-mysqldb

## Usage

- To add or remove element from database, send post request to /update url
- To read from database, send get request to /server/1 for server1, /server/2 for server 2 etc.

## Authors

Darko Dekan

## Unlicence
Look at UNLICENSE.txt file.
