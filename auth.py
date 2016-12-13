#-*- coding:utf-8 -*-
import tweepy
import os
from simple_aes_cipher import AESCipher,generate_secret_key

class TwiAuth:
	api = None
	def authpass(self):
		filename = "auth"
		if os.path.isfile(filename):
			#storeされたtoken使用
			passwd = getpass("keyring password: ")
			source = open(filename,"r").readline().strip()
			cipher = AESCipher(passwd)
			token = cipher.decrypt(source)
			self.api = login_token(token)
			if api is None:
				print("invalid password. exiting...")
				exit(0)
		else:
			#token取得
			token = login_redirect()
			if token != None:
				#保存するか確認
				ans = raw_input("Would you store login with password keyring?: ")
				if ans == "y" or ans == "yes":
					store_token(token)
				else:
					pass
				self.api = login_token(token)
			else:
				print("Login failed. exiting...")
				exit(0)
		if self.api != None:
			print("Login succeeded.")
		else:
			print("ERROR something has gone wrong.")
			exit(1)
	def login_pin(self):
		#auth object(CONSUMER_KEY,CONSUMER_SECRETの順)
		auth = tweepy.OAuthHandler("XVdqky7rKjXqQejbsHJACw89Q",
		"idXcVZAzciyVsMgjQkGqPKLNG092WoPbxVke3xYqmA1lVGm4gC")
		#URL取得
		auth_url = auth.get_authorization_url()
		#行かせる
		print("Get your veification code from " + auth_url)
		#codeを回収
		auth_code = raw_input("Type the code:").strip()
		#token取得
		try:
			auth.get_access_token(auth_code)
		except tweepy.TweepError:
			print("Error! failed to login. exiting...")
			exit(1)
		#tokenをtupleで返す(authもlogin_token用に返す)
		return (auth.access_token, auth.access_token_secret, auth)
	def login_redirect(self):
		#auth object(CONSUMER_KEY,CONSUMER_SECRETの順)
		auth = tweepy.OAuthHandler("XVdqky7rKjXqQejbsHJACw89Q",
		"idXcVZAzciyVsMgjQkGqPKLNG092WoPbxVke3xYqmA1lVGm4gC")
		#公式Snippetからすこしかりた
		# Redirect user to Twitter to authorize
		redirect_user(auth.get_authorization_url())
		# Get access token
		auth.get_access_token("verifier_value")
		#tokenをtupleで返す(authもlogin_token用に返す)
		return (auth.access_token, auth.access_token_secret, auth)
	def login_token(self,token):
		#tokenをセットし、APIインスタンスを返す
		auth = token[2]
		auth.set_access_token(token[0], token[1])
		return tweepy.API(auth)
