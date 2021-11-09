from flask import Flask, request
from flask import render_template
import requests

app = Flask(__name__) # 플라스크 어플리케이션 생성 코드

@app.route('/') # 특정 url에 접속하면 다음 줄에 있는 함수를 호출
def main():
	return render_template("index.html")

@app.route('/result', methods= ['POST', 'GET'])
def inputData():
	data = request.args.get('data', default = 'ns-abc-aaa', type = str)
	print(data)
	return render_template('index.html', data=data)

@app.route('/id/<id>') # 특정 url에 접속하면 다음 줄에 있는 함수를 호출
def getPrice(id):
	detail_url = f'https://place.map.kakao.com/main/v/{id}' # id가 들어가면 json 형태로 넘어옴

	data = requests.get(detail_url).json()

	if 'menuInfo' not in data:
		return -1 # 에러 발생

	menu_list = data['menuInfo']['menuList']
	maxPrice = 0
	maxMenu = ""
	minPrice = 1000000000
	minMenu = ""
	for menu_item in menu_list:
		price = 0
		menu = ''
		if 'price' in menu_item:
			try:
				price = int(menu_item['price'].replace(',', '')) # 가격을 int형변환
				menu = menu_item['menu']
			except:
				continue
			
		if price > maxPrice:
			maxPrice = price
			maxMenu = menu
		if price < 5000:
			continue
		elif price < minPrice:
			minPrice = price
			minMenu = menu
	
	data = { # JSON 형태로 데이터를 반환
		"minMenu":minMenu, "minPrice":minPrice, "maxMenu":maxMenu, "maxPrice":maxPrice
	}
	return data

if __name__ == "__main__": # 직접 실행이면 웹 서버 실행
	app.run(host="0.0.0.0", port=5500, debug=False)