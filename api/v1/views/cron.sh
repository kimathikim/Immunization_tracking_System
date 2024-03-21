#!/bin/bash
export IMS_MYSQL_USER=atas
export IMS_MYSQL_PWD=Team_Project
export IMS_MYSQL_HOST=localhost
export IMS_MYSQL_DB=immunization
python3 -m api.v1.views.notification_sys