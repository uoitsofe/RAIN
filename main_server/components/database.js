"use strict"

const { logger } = require('./logger')
const path = require("path")
const fs = require('fs')
const db = require('diskdb')
const moment = require('moment-timezone')

class Database {
    constructor() {
        this.database = null
        this.db_path = path.join(__dirname, '..', 'data')
        this.DATABASE_TABLES = ['cache'].map(element => `raindata_${element}`)
        this.connectToDatabase()
    }
    static getInstance() {
        if (!!!this.instance) {
            this.instance = new Database()
        }
        return this.instance
    }
    connectToDatabase() {
        logger.info("Start Loading DB...")
        if (!fs.existsSync(this.db_path)) {
            fs.mkdirSync(this.db_path)
            logger.info("create dir for db")
        }
        logger.info("Connecting to db...")
        this.database = db.connect(this.db_path, this.DATABASE_TABLES)
        logger.info("Connected to db")
    }
    clearAndDisconnect() {
        this.DATABASE_TABLES.forEach(element => this.database[element].remove())
    }
    getDatabase() {
        return this.database
    }
    getEverything() {
        return this.database.raindata_cache.find()
    }
    insertPredictedData(data) {
        data.forEach(element => {
            this.database.raindata_cache.save(element)
        })
    }
}

module.exports = {
    Database
}