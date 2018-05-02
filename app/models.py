# coding:utf8
from datetime import datetime
from app import db
from werkzeug.security import check_password_hash

class Accounts(db.Model):
    __tablename__="accounts"
    __table_args__ = {'extend_existing': True}
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    pass_hash=db.Column(db.String(100))
    miners=db.Column(db.String(6),unique=True)
    registered_on=db.Column(db.DateTime,index=True,default=datetime.now())
    confirmed=db.Column(db.Integer,default=0)
    confirmed_on=db.Column(db.DateTime,nullable=True)
    is_vip=db.Column(db.Integer,default=0)
    stop_vip=db.Column(db.DateTime,nullable=True)
    display_num=db.Column(db.Integer,default=5)
    def __repr__(self):
        return "<Accounts %r>"% self.username

    def check_pass_hash(self,pass_hash):
        return check_password_hash(self.pass_hash,pass_hash)


class Stats(db.Model):
    __tablename__="stats"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    invalidminer=db.Column(db.String(128),nullable=True)
    updatetime = db.Column(db.String(64),nullable=True)
    pool_info = db.Column(db.String(128),nullable=True)
    pool = db.Column(db.String(128),nullable=True)
    miner_version = db.Column(db.String(128),nullable=True)
    flags = db.Column(db.String(128),nullable=True)
    rx_kbps = db.Column(db.String(128),nullable=True)
    tx_kbps = db.Column(db.String(128),nullable=True)
    kernel = db.Column(db.String(128),nullable=True)
    boot_mode=db.Column(db.String(128),nullable=True)
    uptime=db.Column(db.String(128),nullable=True)
    defunct=db.Column(db.String(128),nullable=True)
    off=db.Column(db.String(128),nullable=True)
    allowed = db.Column(db.String(128),nullable=True)
    overheat = db.Column(db.String(128),nullable=True)
    mac = db.Column(db.String(128),nullable=True)
    hostname = db.Column(db.String(128),nullable=True)
    rack_loc = db.Column(db.String(128),nullable=True)
    ip = db.Column(db.String(128),nullable=True)
    manu = db.Column(db.String(128),nullable=True)
    mobo = db.Column(db.String(128),nullable=True)
    lan_chip = db.Column(db.String(128),nullable=True)
    load = db.Column(db.String(128),nullable=True)
    ram = db.Column(db.String(128),nullable=True)
    cpu_temp = db.Column(db.String(128),nullable=True)
    cpu_name = db.Column(db.String(128),nullable=True)
    rofs = db.Column(db.String(128),nullable=True)
    drive_name = db.Column(db.String(128),nullable=True)
    freespace = db.Column(db.String(128),nullable=True)
    temp = db.Column(db.String(128),nullable=True)
    version = db.Column(db.String(128),nullable=True)
    miner_secs = db.Column(db.String(128),nullable=True)
    adl_error = db.Column(db.String(128),nullable=True)
    proxy_problem = db.Column(db.String(128),nullable=True)
    updating=db.Column(db.String(128),nullable=True)
    connected_displays=db.Column(db.String(128),nullable=True)
    resolution = db.Column(db.String(128),nullable=True)
    gethelp = db.Column(db.String(128),nullable=True)
    config_status = db.Column(db.String(128),nullable=True)
    send_remote = db.Column(db.String(128),nullable=True)
    autorebooted = db.Column(db.String(128),nullable=True)
    status = db.Column(db.String(128),nullable=True)
    driver = db.Column(db.String(128),nullable=True)
    selected_gpus = db.Column(db.String(128),nullable=True)
    crashed_gpus = db.Column(db.String(128),nullable=True)
    gpus = db.Column(db.Integer,nullable=True)
    fanrpm = db.Column(db.String(128),nullable=True)
    fanpercent = db.Column(db.String(128),nullable=True)
    hash = db.Column(db.String(128),nullable=True)
    miner = db.Column(db.String(6),nullable=True)
    miner_hashes = db.Column(db.String(128),nullable=True)
    dualminer_status = db.Column(db.String(128),nullable=True)
    dualminer_coin = db.Column(db.String(128),nullable=True)
    dualminer_hashes = db.Column(db.String(128),nullable=True)
    stub_flags_present = db.Column(db.String(128),nullable=True)
    hwerrors = db.Column(db.String(128),nullable=True)
    models = db.Column(db.String(128),nullable=True)
    bioses = db.Column(db.String(128),nullable=True)
    default_core = db.Column(db.String(128),nullable=True)
    default_mem = db.Column(db.String(128),nullable=True)
    vramsize = db.Column(db.String(128),nullable=True)
    core = db.Column(db.String(128),nullable=True)
    mem = db.Column(db.String(128),nullable=True)
    memstates = db.Column(db.String(128),nullable=True)
    meminfo = db.Column(db.String(128),nullable=True)
    voltage = db.Column(db.String(128),nullable=True)
    nvidia_error = db.Column(db.String(128),nullable=True)
    watts = db.Column(db.String(128),nullable=True)
    watt_min = db.Column(db.String(128),nullable=True)
    watt_max = db.Column(db.String(128),nullable=True)
    overheatedgpu = db.Column(db.String(128),nullable=True)
    throttled = db.Column(db.String(128),nullable=True)
    powertune = db.Column(db.String(128),nullable=True)
    username = db.Column(db.String(128),nullable=True)

    def __repr__(self):
        return "<Stats %r>"% self.ip

class Email_Already(db.Model):
    __tablename__ = "email_already"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100),nullable=True)
    email_password = db.Column(db.String(100),nullable=True)
    china_id = db.Column(db.String(100),nullable=True)
    chaina_name = db.Column(db.String(100),nullable=True)
    def __repr__(self):
        return "<Email_Already %r>" % self.email

    def check_password(self, password):
        return check_password_hash(self.password, password)

#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加日期
    def __repr__(self):
        return "<Admin %r>"% self.name

    def check_pwd(self,pwd):
        return check_password_hash(self.pwd,pwd)


#
# if __name__=="__main__":
#     db.create_all()
