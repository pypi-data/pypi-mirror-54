
### Django Json Tools

```python        

# http_response_json_models(ser, data, code, msg)    
# 栗子:        
class get_user_info(APIView):            
	user = User.object.get(pk=1)            
	return http_response_json_models(UserSerializer, user, 1, '查询用户信息成功') 

# {'code':1, msg: '查询用户信息成功', data: {'id':1, 'username': 'ingrun'} }
：：:
```


