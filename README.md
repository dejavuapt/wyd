# Tracking yours doing every hour.

### bot tracking v0.1

```bash
py -m venv env 
./env/Scripts/activate 

pip install -r requirements.txt 
```

also you need a file with your token
just take `template_constants.py` to `app/constants.py`
and rename str to your TG bot token

---

next updates:
v0
- [x] reminder every hour static time
    - [x] check if `start_callbalck` call earlier
    - [ ] dynamic set time from command
    - [ ] dynamic set weekday from command
- [x] stop reminder in today
    - [ ] check if `stop_callbalck` call earlier
    - [ ] choose stop today reminder or all reminder
- [ ] localization
- [ ] add command to get statistic

v1  
- [ ] parser of `doing` command user text
    - [ ] template by regex? 
    - [ ] temperory write in csv file