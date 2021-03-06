#coding=utf-8
"""filename:app/models.py
Created 2017-05-30
Author: by anaf
note:数据库模型函数
"""

from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from flask_login import UserMixin,AnonymousUserMixin
from .import login_manager
from datetime import datetime
import hashlib,random
from flask import request,current_app
import datetime as datetime2



#权限,必须进二阶乘 *2  0x10,0x20,0x40,0x80
class Permission:
	FOLLOW = 0x01   #关注
	COMMIT = 0x02	#在他人的文章中发表评论
	WRITE_ARTICLES = 0x03	#写文章
	MODERATE_COMMENTS = 0x04 #管理他人发表的评论
	DRIVER = 0x08  #司机栏目
	CONSIGNOR =0x10 #货主栏目
	ADMINISTER = 0x80	#管理员
	SUPERADMIN = 0x80	#超级管理员


"""角色表 一对多，一个角色对应多个用户
db.relationship('User',backref='role')
因为User 还没有定义 所以使用字符串形式指定
"""
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	default = db.Column(db.Boolean,default=False,index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User',backref='role',lazy='dynamic')

	def __repr__(self):
		return self.name

	@staticmethod
	def insert_roles():
		#二进制处理的所以在数据库中显示的7、255、3
		roles = {
			u'普通用户':(Permission.FOLLOW|
					Permission.COMMIT|
					Permission.WRITE_ARTICLES,True),

			u'管理员':(Permission.FOLLOW|
					Permission.COMMIT|
					Permission.WRITE_ARTICLES|
					Permission.MODERATE_COMMENTS,False),

			u'司机':(Permission.FOLLOW|
					Permission.COMMIT|
					Permission.WRITE_ARTICLES|
					Permission.DRIVER,False),

			u'货主':(Permission.FOLLOW|
					Permission.COMMIT|
					Permission.WRITE_ARTICLES|
					Permission.CONSIGNOR,False),

			u'超级管理员':(0xff,False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()


class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key = True)
	#账户名称
	username = db.Column(db.String(64),unique=True,index=True)
	#密码
	password_hash = db.Column(db.String(128))
	#支付密码
	pay_pwd_hash = db.Column(db.String(128),default='')
	#创建时间
	member_since = db.Column(db.DateTime(),default=datetime.now)
	#最后访问时间
	last_seen = db.Column(db.DateTime(),default=datetime.now)
	#电子邮箱，找回密码
	mail = db.Column(db.String(100),unique=True) 
	#手机号，也可以用于登陆
	phone  = db.Column(db.String(100),index=True,unique=True)
	#账户资金
	price  = db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None),default=0)
	#账户锁定资金
	lock_price  = db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None),default=0)
	#状态  默认1
	status = db.Column(db.Integer(),default=1)

	#头像哈希
	avatar_hash = db.Column(db.String(32))
	#微信openid
	wx_open_id = db.Column(db.String(100))
	#角色，多对一
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
	
	#货主表 一对一   uselist=False
	consignors  = db.relationship('Consignor', backref='user',uselist=False)
	#创建者负责人  多对一  relationship  不会在表中显示行
	drivers  = db.relationship('Driver', backref='user',lazy='dynamic')
	#车队
	fleet_id  = db.Column(db.Integer())
	
	#货物发布者 这里不做货物发布了   货物发布应当链接到货主表
	# goods_id = db.relationship('Goods',backref='user_goods',primaryjoin='Goods.user_id == User.id')
	#货物司机接单者
	car_goods_id = db.relationship('Goods',backref='user',lazy='dynamic')
	#付款者
	order_pays = db.relationship('Order_pay', backref='user',lazy='dynamic')
	#用户邮件
	user_msgs = db.relationship('User_msg', backref='user',lazy='dynamic')
	#一对一 用户信息表
	user_infos  = db.relationship('User_info', backref='user',uselist=False)
	#用户位置表
	positions = db.relationship('Position', backref='user',lazy='dynamic')
	#用户优惠券
	couponsed = db.relationship('Coupons', backref='user')
	#提现shenqing
	tixianchengqings = db.relationship('Tixianchengqing', backref='user',lazy='dynamic')
	#提现打款操作员
	# tixiancaozuoyuan = db.relationship('Tixianchengqing', backref='caozuoyuan',lazy='dynamic')
	#是否已经允许定位  0未允许   1已允许
	is_location = db.Column(db.Integer,default=0)
	

	def __init__(self,**kwargs):
		super(User,self).__init__(**kwargs)
		#初始化时候添加自己为关注者
		#self.follow(self)
		#赋予角色信息
		if self.role is None:
			if self.username == current_app.config['SUPERADMIN_NAME']:
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()


	def __unicode__(self):
		return self.phone

	#头像
	def gravatar(self,size=100,default='identicon',rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
		hash = self.avatar_hash or hashlib.md5(self.username.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
				url=url,hash=hash,size=size,default=default,rating=rating)



	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	@property
	def pay_pwd(self):
		raise AttributeError('pay_pwd is not a readable attribute')

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	@pay_pwd.setter
	def pay_pwd(self,pay_pwd):
		self.pay_pwd_hash = generate_password_hash(pay_pwd)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)
	def verify_pay_pwd(self,pay_pwd):
		return check_password_hash(self.pay_pwd_hash,pay_pwd)

	#验证角色
	def can(self,permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permissions

	#管理员
	def is_administrator(self):
		return self.can(Permission.ADMINISTER)
	def is_superadmin(self):
		return self.can(Permission.SUPERADMIN)

	#刷新用户最后访问时间
	def ping(self):
		self.last_seen = datetime.now()
		db.session.add(self)

#用户信息表
class User_info(db.Model):
	__tablename__ = 'user_infos'
	id = db.Column(db.Integer,primary_key=True)	
	#姓名
	name = db.Column(db.String(64),default='')	
	#真实姓名
	lastname = db.Column(db.String(64),default='')	
	#信用等级
	level = db.Column(db.Integer,default=1)
	#信息登录 1未认证 2已认证 3系统设置诚信会员 -1黑名单 
	info_level = db.Column(db.Integer,default=1)
	#推荐人数 
	recommended = db.Column(db.Integer,default=0)
	#下单次数
	order_times = db.Column(db.Integer,default=0)
	#接单次数
	order_number = db.Column(db.Integer,default=0)
	#违约次数
	treaty_number = db.Column(db.Integer,default=0)
	#用户积分
	source = db.Column(db.Integer,default=0)
	#申请认证时间
	cif_time = db.Column(db.DateTime())
	#确认时间
	confirm_time = db.Column(db.DateTime())
	#银行卡所属银行
	suoshuyinhang = db.Column(db.String(64),default='')	
	kaihuhang = db.Column(db.String(200),default='')	
	kahao = db.Column(db.String(64),default='')	

	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

#用户位置表
class Position(db.Model):
	__tablename__ = 'positions'
	id = db.Column(db.Integer,primary_key=True)	
	latitude = db.Column(db.String(64))	
	longitude = db.Column(db.String(64))	
	precision = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))


#提现申请
class Tixianchengqing(db.Model):
	__tablename__ = 'tixianchengqings'
	id = db.Column(db.Integer,primary_key=True)	
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	caozuoyuan_id = db.Column(db.String(200))
	#备注
	note = db.Column(db.String(200))
	#金额
	price = db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None),default=0)
	#申请时间
	create_time = db.Column(db.DateTime(),default=datetime.now)
	#完成时间
	finish_time = db.Column(db.DateTime())
	#状态 0创建申请，1进行中 2完成
	state = db.Column(db.Integer,default=0)


#优惠券
class Coupons(db.Model):
	__tablename__ = 'couponsion'
	id = db.Column(db.Integer,primary_key=True)	
	#优惠金额
	price = db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None),default=0)
	#条件 大于多少才能使用
	maxprice = db.Column(db.Integer,default=100)
	#状态  1可使用 2已使用 0不可用
	state = db.Column(db.Integer,default=1)
	#创建时间
	create_time = db.Column(db.DateTime,default=datetime.now)
	#过期时间
	expiration_time = db.Column(db.DateTime)
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

	# def __unicode__(self):
	# 	return self.price
		

"""
class User_level(db.Model):
	__tablename__ = 'user_level'
	id = db.Column(db.Integer,primary_key=True)	
	#等级名称  一星会员 二星会员
	name = db.Column(db.String(64))	 
	#资费优惠 百分比
	discounts = db.Column(db.String(10))
	#快捷发布条数
	count = db.Column(db.Integer)	 
"""


#验证角色
class AnonymousUser(AnonymousUserMixin):
	def can(self,permissions):
		return False

	def is_administrator(self):
		return False
#验证角色
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



#用户消息表
class User_msg(db.Model):
	__tablename__ = 'user_msgs'
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(64))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime(),default=datetime.now)
	#是否显示？
	show = db.Column(db.Integer,default=0)
	#状态0已发送未读 1已读 -1删除 2已确认,已确认跟已读区别就是已确认就是支付内容一定的删除了
	state = db.Column(db.Integer())
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


"""
使用者    负责人    车辆
A		A			A
B		A			A
C		A			A	
A		B			B
B		A			C

1.一辆车只有一个负责人
2.一辆车可以有多个使用者
3.一个负责人可以有多台车

"""

driver_user_reg = db.Table('driver_user_reg',
						db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
						db.Column('use_driver_id',db.Integer,db.ForeignKey('drivers.id'))
					)


#车辆表
class Driver(db.Model):
	__tablename__ = 'drivers'
	id = db.Column(db.Integer(),primary_key=True)
	# 创建者主人# 多对一    会在表中创建user_id
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	#创建者  多，     一辆车 多个人用
	use = db.relationship('User',
								secondary=driver_user_reg,
								backref=db.backref('use_drivers', lazy='dynamic'),
								lazy='dynamic')
	
	# users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	#车长
	length = db.Column(db.String(255))
	#车型
	car_type = db.Column(db.String(255))
	#体积
	tiji = db.Column(db.String(255))
	#重量
	zhongliang = db.Column(db.String(255))
	#品牌
	# brand =  db.Column(db.String(255))
	#车牌号
	number = db.Column(db.String(255))
	#车架号码
	frame_number  = db.Column(db.String(255))
	#发动机号码
	engine_number  = db.Column(db.String(255))
	#行驶证
	driver   = db.Column(db.String(255))
	#驾驶证
	travel   = db.Column(db.String(255))
	#违约次数
	break_number = db.Column(db.Integer(),default=0) 
	#申请时间
	create_time = db.Column(db.DateTime,default=datetime.now) 
	#开通时间
	start_time = db.Column(db.DateTime,default=datetime.now) 
	#状态 0未申请 1已申请   2已开通
	state = db.Column(db.Integer(),default=0)
	#车辆描述
	note = db.Column(db.Text)
	#车辆证件照片   一
	driver_images = db.relationship('Driver_images', backref='driver',lazy='dynamic')
	#直接关联车辆信息表driver_posts ,2017-07-21-司机自助下单  直接关联这个表不用发布信息所以不用关联下面这个了
	order_pays = db.relationship('Order_pay', backref='driver',lazy='dynamic')
	driver_posts = db.relationship('Driver_post', backref='driver',lazy='dynamic')
	#司机自助下单货物用户
	driver_self_orders = db.relationship('Driver_self_order', backref='driver',lazy='dynamic')

	# def __unicode__(self):
	# 	return self.number

	def __unicode__(self):
		return self.number



	# def __repr__(self):
	# 	return self.number


#车辆照片
class Driver_images(db.Model):
	__tablename__ = 'driver_images'
	id = db.Column(db.Integer(),primary_key=True)
	name = db.Column(db.String(64)) #
	url = db.Column(db.String(100))
	#多
	driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))


#货主表发货人。不是goods货源表
class Consignor(db.Model):
	__tablename__ = 'consignors'
	id = db.Column(db.Integer(),primary_key=True)
	# 创建者主人# 多对一    会在表中创建user_id
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	#公司名称
	name = db.Column(db.String(64),default='')
	#负责人名字
	fuzheren = db.Column(db.String(64),default='')
	#负责人身份证号
	shenfenzheng = db.Column(db.String(64),default='')
	#公司大小规模 人数  20人  50人100人200人 500人1000人 2000人10000人
	company_size = db.Column(db.String(50),default='') 
	#公司行业，水产，销售 木材。。等等
	company_industry = db.Column(db.String(50),default='') 
	#证件表  ，公司营业执照等证件。
	# company_cer = db.Column(db.Integer()) 
	#公司地址
	address  = db.Column(db.String(255),default='') 
	#违约次数
	break_number = db.Column(db.Integer(),default=0) 
	#申请时间
	create_time = db.Column(db.DateTime,default=datetime.now) 
	#开通时间
	start_time = db.Column(db.DateTime,default=datetime.now) 
	#状态 0未开通 1申请中 2已通过
	state = db.Column(db.Integer(),default=0)
	#公司简介
	note = db.Column(db.Text,default='')
	#接单车辆？ 接的是  车辆信息表
	# driver_post = db.relationship('Driver_post', backref='driver_posts',lazy='dynamic',primaryjoin='Driver_post.consignor_user_id == Consignor.id')
	#货物表
	goodsed = db.relationship('Goods', backref='consignor',lazy='dynamic')
	#货主自助下单   
	goods_self_orders = db.relationship('Goods_self_order', backref='consignor',lazy='dynamic')
	consignor_imagesed = db.relationship('Consignor_images', backref='consignor',lazy='dynamic')

	def __unicode__(self):
		return self.name
	

#货主照片
class Consignor_images(db.Model):
	__tablename__ = 'consignor_images'
	id = db.Column(db.Integer(),primary_key=True)
	name = db.Column(db.String(64)) #
	url = db.Column(db.String(100))
	#多
	consignor_id = db.Column(db.Integer, db.ForeignKey('consignors.id'))

#货主发布的货物信息表
class Goods(db.Model):
	__tablename__ = 'goods'
	id = db.Column(db.Integer(),primary_key=True)
	#名称
	name = db.Column(db.String(255)) 
	#体积 方
	tiji = db.Column(db.String(16)) 
	#重量
	zhongliang = db.Column(db.String(16)) 
	#车型
	car_type = db.Column(db.String(16)) 
	#车长
	car_length = db.Column(db.String(16)) 
	#单位  （吨，千克，次[趟]）
	unit = db.Column(db.String(16)) 
	#数量
	count = db.Column(db.Integer(),default=1)
	#发货地
	start_address = db.Column(db.String(255)) 
	start_sheng = db.Column(db.String(255)) 
	start_shi = db.Column(db.String(255)) 
	start_qu = db.Column(db.String(255)) 
	start_xiangxi_address = db.Column(db.String(255)) 
	#运送地
	end_address = db.Column(db.String(255)) 
	end_sheng = db.Column(db.String(255)) 
	end_shi = db.Column(db.String(255)) 
	end_qu = db.Column(db.String(255)) 
	end_xiangxi_address = db.Column(db.String(255)) 
	#描述
	note = db.Column(db.Text) 
	#car_type 整车拼车零担
	select_car_type = db.Column(db.String(255)) 
	#发车时间
	start_car_time =  db.Column(db.DateTime) 
	start_zone = db.Column(db.String(10))
	#发布时间
	create_time = db.Column(db.DateTime,default=datetime.now) 
	#发布者 不是user表 应该是货主公司表 
	consignors_id = db.Column(db.Integer, db.ForeignKey('consignors.id'))
	# user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	#开始报价运费
	start_price = db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None))
	#实际运费   接单结算运费 定金抽取比例在订单列表  系统调节
	end_price =  db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None))
	#接单者
	car_user_id =  db.Column(db.Integer, db.ForeignKey('users.id'))
	# #对应车辆信息表
	driver_posts = db.relationship('Driver_post', backref='goodsed',lazy='dynamic')
	# derver_posts_id =  db.Column(db.Integer, db.ForeignKey('driver_post.id'))
	#接单时间
	receive_time = db.Column(db.DateTime) 
	#状态 -2失效订单超时未支付  -1管理员关闭 0发布 
	#1司机已经接单未付款 ，2司机已付款到系统  
	#3司机已经运送抵达ok  4系统或货主确认已经抵达ok 完成  
	#5货主确认了司机的接单信息   。其他状态等待 ?
	state = db.Column(db.Integer(),default=0)
	order_pays = db.relationship('Order_pay', backref='goodsed',lazy='dynamic')
	#预约数量
	make_count = db.Column(db.Integer,default=0)
	#紧急状态 置顶1
	show_statie = db.Column(db.Integer,default=0)
	#自助下单
	driver_self_posts = db.relationship('Driver_self_order', backref='goodsed',lazy='dynamic')
	#是否在线支付运费  默认1在线支付
	online_pirce = db.Column(db.Integer,default=1)
	#货主是否已经支付运费。  默认未支付
	price_is_pay = db.Column(db.Integer,default=0)

	def __unicode__(self):
		return u'ID:'+str(self.id)



#支付订单表，一次交易有两条，一条货主支付运费，线下交易金额为0，一条司机支付定金
class Order_pay(db.Model):
	__tablename__ = 'order_pays'
	id = db.Column(db.Integer,primary_key=True)
	#订单
	order  = db.Column(db.String(30),unique=True)
	#货物
	goods_id =  db.Column(db.Integer, db.ForeignKey('goods.id'))
	#车辆
	drivers_id =  db.Column(db.Integer, db.ForeignKey('drivers.id'))
	#车运信息
	driver_post_id =  db.Column(db.Integer, db.ForeignKey('driver_posts.id'))
	#创建时间
	create_time = db.Column(db.DateTime,default=datetime.now)
	#支付时间
	pay_time = db.Column(db.DateTime)
	#-1失效 0创建 1审核通过未支付 2已支付 
	state = db.Column(db.Integer,default=0)
	#支付者，一个是货主  一个是  司机  
	pay_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	#支付金额
	pay_price = db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None))
	#订单标记  货主支付运费  司机支付 定金
	note = db.Column(db.String(50))


#车运信息
class Driver_post(db.Model):
	__tablename__ = 'driver_posts'
	id = db.Column(db.Integer,primary_key=True)
	#名称
	title = db.Column(db.String(100))
	#发车地点
	#出发省
	start_sheng = db.Column(db.String(100))
	#出发市
	start_shi = db.Column(db.String(100))
	#出发区
	start_qu = db.Column(db.String(100))

	#目的省
	end_sheng = db.Column(db.String(100))
	#目的省
	end_shi = db.Column(db.String(100))
	#目的省
	end_qu = db.Column(db.String(100))

	#描述
	note = db.Column(db.Text) 
	#发车时间
	start_car_time =  db.Column(db.DateTime) 
	#发车时段  全天 上午下午晚上
	zone = db.Column(db.String(100))

	start_address = db.Column(db.String(200))
	#目的省
	end_address = db.Column(db.String(200))

	#发布时间
	create_time = db.Column(db.DateTime,default=datetime.now) 
	#发布者
	driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
	#开始报价运费
	start_price = db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None))
	#实际运费   接单结算运费 系统抽取比例  系统调节
	end_price =  db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None))
	# #接单者，关联到货物信息表
	consignor_id =  db.Column(db.Integer, db.ForeignKey('goods.id'))
	#接单时间
	receive_time = db.Column(db.DateTime) 
	#状态 -2失效订单被抢付  -1管理员关闭 0发布 1司机已经接单未付款 ，2司机已付款到系统  3已经运送抵达ok  4司机自身去接单，所以该条信息自动冲掉 ！5！其他状态等待
	state = db.Column(db.Integer(),default=0)
	#外键订单列表
	order_pays = db.relationship('Order_pay', backref='driver_post')

	goods_self_orders = db.relationship('Goods_self_order', backref='driver_post',lazy='dynamic')
	#预约次数
	make_count = db.Column(db.Integer,default=0)



#车辆信息  车长  体积 方   重量 吨  不做外键。
class Car_Info(db.Model):
	__tablename__ = 'car_infos'
	id = db.Column(db.Integer,primary_key=True)
	length = db.Column(db.String(80))
	tiji = db.Column(db.String(80))
	zhongliang = db.Column(db.String(80))
	sort = db.Column(db.Integer,default=10)

#车型  低栏 平板 高栏 冷藏车 等   不做外键
class Car_Type(db.Model):
	__tablename__ = 'car_types'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80))

#司机自助下单 货物预约表
class Driver_self_order(db.Model):
	__tablename__ = 'driver_self_orders'
	id = db.Column(db.Integer,primary_key=True)
	driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
	goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
	create_time = db.Column(db.DateTime,default=datetime.now)
	#状态默认0 1审核通过  一般一条货物信息只有一个是审核通过的 ,2司机不接单 3货主同意该预约
	state = db.Column(db.Integer(),default=0)
	#预约价格
	price =  db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None))

	# def __unicode__(self):
	# 	return self.driver_id

#货主自助下单 车辆预约表
class Goods_self_order(db.Model):
	__tablename__ = 'goods_self_orders'
	id = db.Column(db.Integer,primary_key=True)
	driver_post_id = db.Column(db.Integer, db.ForeignKey('driver_posts.id'))
	consignors_id = db.Column(db.Integer, db.ForeignKey('consignors.id'))
	create_time = db.Column(db.DateTime,default=datetime.now)
	#状态默认0 1审核通过  一般一条货物信息只有一个是审核通过的
	state = db.Column(db.Integer(),default=0)
	#预约价格
	price =  db.Column(db.Numeric(precision=10,scale=2,\
		asdecimal=True, decimal_return_scale=None))


#定时任务表
class Scheduler_task(db.Model):
	__tablename__ = 'scheduler_tasks'
	id = db.Column(db.Integer,primary_key=True)
	#任务名称
	func_id = db.Column(db.String(200))
	#创建时间  执行时间
	create_time = db.Column(db.DateTime)
	#函数名称
	func = db.Column(db.String(100))
	#参数  货源的id
	args = db.Column(db.String(200))


#还有推荐
class Haoyoutuijian(db.Model):
	__tablename__ = 'haoyoutuijians'
	id = db.Column(db.Integer,primary_key=True)
	tuijianren = db.Column(db.Integer)
	beituijianren = db.Column(db.Integer)
	create_time = db.Column(db.DateTime,default=datetime.now)


	
