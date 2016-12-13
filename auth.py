#-*- coding:utf-8 -*-
import tweepy
import os
from getpass import getpass
from simple_aes_cipher import AESCipher,generate_secret_key

class TwiAuth:
	api = None
	def authpass(self):
		filename = "auth"
		if os.path.isfile(filename):
			#storeされたtoken使用
			token = self.load_token(filename)
			self.api = self.login_token(token)
			if self.api is None:
				print("invalid password. exiting...")
				exit(0)
		else:
			#token取得
			token = self.login_code()
			if token != None:
				#保存するか確認
				ans = input("Would you store login with password keyring?: ")
				if ans == "y" or ans == "yes":
					self.store_token(filename,token)
				else:
					pass
				self.api = self.login_token(token)
			else:
				print("Login failed. exiting...")
				exit(0)
		if self.api != None:
			print("Login succeeded.")
		else:
			print("ERROR something has gone wrong.")
			exit(1)
	def login_code(self):
		#auth object(CONSUMER_KEY,CONSUMER_SECRETの順)
		auth = tweepy.OAuthHandler("XVdqky7rKjXqQejbsHJACw89Q",
		"idXcVZAzciyVsMgjQkGqPKLNG092WoPbxVke3xYqmA1lVGm4gC")
		#URL取得
		auth_url = auth.get_authorization_url()
		#行かせる
		print("Get your veification code from " + auth_url)
		#codeを回収
		auth_code = input("Type the code:").strip()
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
		#公式Snippetからすこしかりた(けど、メソッド未定義でつかえない)
		# Redirect user to Twitter to authorize -> ????
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
	def store_token(self,filename,token):
		passwd = getpass("Tell me storing password:")
		verify_passwd = getpass("Verify password:")
		if passwd == verify_passwd:
			#token,token_secのみ書き込む
			sec_key = generate_secret_key(passwd)
			cipher = AESCipher(sec_key)
			dstfile = open(filename,"w")
			keyfile = open(filename+"_key","wb")
			keyfile.write(sec_key)
			dstfile.write(cipher.encrypt(token[0])+"\n")
			dstfile.write(cipher.encrypt(token[1])+"\n")
			dstfile.close()
			keyfile.close()
			print("Login successfly stored.")
		else:
			print("password mismatch!")
			store_token(token)
	def load_token(self,filename):
		passwd = getpass("keyring password: ")
		srcfile = open(filename,"r")
		keyfile = open(filename+"_key","rb")
		source = srcfile.readlines()
		key_source = keyfile.readline()
		srcfile.close()
		keyfile.close()
		source = list(map(lambda s: s.strip(),source))
		cipher = AESCipher(key_source)
		raw_token = (cipher.decrypt(source[0]), cipher.decrypt(source[1]))
		auth = (tweepy.OAuthHandler("XVdqky7rKjXqQejbsHJACw89Q",
		"idXcVZAzciyVsMgjQkGqPKLNG092WoPbxVke3xYqmA1lVGm4gC"),)
		token = raw_token + auth
		return token
