#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: kevin <304050118@qq.com>

import rospy
import os
import sys
import time
from threading import Timer
from audio_common_msgs.msg import AudioData
from rikibot_ai_speech import RikibotAISpeech
from geometry_msgs.msg import Twist
from glm import get_intitude

class RikibotVoice(object):
    def __init__(self):
        self.register_code = os.environ['RIKI_SERIAL']
        self.sub_audio = rospy.Subscriber("speech_audio", AudioData, self.audio_cb)
        self.pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = self.dir_path.replace('rikibot_ai_speech/nodes', 'rikibot_ai_speech/')
        self.dir_path += 'voice/'
        self.device_id = rospy.get_param("~device_id", 24)
        self.timeout = rospy.get_param("~stop_time", 5)
        self.order = [u'前进',u'后退',u'左转',u'右转', u'停止']
        self.history=[]
        self.ai = RikibotAISpeech(self.device_id, self.dir_path, register_code=self.register_code)
        self.audio_text = None
        self.is_canceling = False
        self.linear_x = 0.0
        self.angular_z = 0.0
        self.is_voice = False
        r = rospy.Rate(10)
        move_cmd = Twist()
        while not rospy.is_shutdown():
	    
	    if self.is_voice is True:
		    self.is_voice = False
            self.is_canceling = True
		    user_text=self.audio_text.encode('utf-8')
		    rospy.loginfo("You Said: %s", user_text)
		    glm_result=get_intitude(user_text,self.history)
		    
		    self.history=glm_result['history']
		    if self.history!=None:
			    for i in range(len(self.history)):
				self.history[i][0]=self.history[i][0].encode('utf-8')
				self.history[i][1]=self.history[i][1].encode('utf-8')
		  
		    index=glm_result['index'].encode('utf-8')
		  
		    if index in ['5','6','7','8','9','10']:
			#print(self.history)
			print(glm_result['response'].encode('utf-8'))
			txt = glm_result['response'].encode('utf-8')
			self.ai.text_to_audio(glm_result['response'].encode('utf-8'))

			self.ai.audio_play()
			
			time.sleep(1)
 			self.is_canceling = False
		    else :
                if index=='0':
                    rospy.loginfo("Rikibot Go Forward")
                    self.linear_x = 0.3
                    self.angular_z = 0.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='1':
                    rospy.loginfo("Rikibot Go Back")
                    self.linear_x = -0.3
                    self.angular_z = 0.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='2':
                    rospy.loginfo("Rikibot Go Left")
                    self.linear_x = 0.0
                    self.angular_z = -1.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='3':
                    rospy.loginfo("Rikibot Go Right")
                    self.linear_x = 0.0
                    self.angular_z = 1.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='4':
                    rospy.loginfo("Rikibot Stop")
                    self.linear_x = 0.0
                    self.angular_z = 0.0
			time.sleep(1)
		    self.is_canceling = False
	    move_cmd.linear.x = self.linear_x
        move_cmd.angular.z = self.angular_z
        self.pub_vel.publish(move_cmd)
	    r.sleep()


    def cbStopvel(self):
        rospy.loginfo("Rikibot Stop")
        self.linear_x = 0.0
        self.angular_z = 0.0
    def audio_cb(self, msg):
        if self.is_canceling is True:
            return

        self.audio_text = self.ai.audio_to_text(msg.data)	
        if self.audio_text is not None:
            self.is_voice = True
    '''
    def audio_cb(self, msg):
        if self.is_canceling is True:
            return

        self.audio_text = self.ai.audio_to_text(msg.data)

        if self.audio_text is not None:
	    
            user_text=self.audio_text.encode('utf-8')
	    rospy.loginfo("You Said: %s", user_text)
            glm_result=get_intitude(user_text,self.history)
	    
            self.history=glm_result['history']
	    if self.history!=None:
		    for i in range(len(self.history)):
			self.history[i][0]=self.history[i][0].encode('utf-8')
			self.history[i][1]=self.history[i][1].encode('utf-8')
            self.is_canceling = True
	    index=glm_result['index'].encode('utf-8')
	  
            if index in ['5','6','7','8','9','10']:
		#print(self.history)
		print(glm_result['response'].encode('utf-8'))
		txt = glm_result['response'].encode('utf-8')
		self.ai.text_to_audio(glm_result['response'].encode('utf-8'))

                self.ai.audio_play()
		
                time.sleep(1)
		
            else :
                if index=='0':
                    rospy.loginfo("Rikibot Go Forward")
                    self.linear_x = 0.3
                    self.angular_z = 0.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='1':
                    rospy.loginfo("Rikibot Go Back")
                    self.linear_x = -0.3
                    self.angular_z = 0.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='2':
                    rospy.loginfo("Rikibot Go Left")
                    self.linear_x = 0.0
                    self.angular_z = 1.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='3':
                    rospy.loginfo("Rikibot Go Right")
                    self.linear_x = 0.0
                    self.angular_z = -1.0
                    Timer(self.timeout, self.cbStopvel).start()
                elif index=='4':
                    rospy.loginfo("Rikibot Stop")
                    self.linear_x = 0.0
                    self.angular_z = 0.0 
            
            self.is_canceling = False
    '''


if __name__ == '__main__':
    rospy.init_node("Rikibot_Voice_Node")
    rikibotai = RikibotVoice()
    rospy.spin()
