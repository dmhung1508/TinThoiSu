import re

rmlist = ['ANTD.VN', 'Dân trí', 'VTC Now', 'VTC1','VTV24', 'VTV.vn', 'Vietnam+',  'VietnamPlus', 'TV24h', 'GĐXH', 'Tạp chí Doanh nghiệp Việt Nam', 'Kênh Ăn Ngủ Bóng Đá cập nhật liên tục', 'UNDP', 'VNEWS', 'PLO', 'Vnexpress', 'Theo: Vnexpress', 'blvquangtung', 'QuanTheThao',
          'ANTV', 'THVN', 'TV4K','quot','Bongda24h', 'Thethaovanhoa.vn', 'âm nhạc', 'Dân trí', 'ANTV','VTC News', 'SCMP', 'tintuc', 'THVN']

special_character = ["▶","🅙","🅑", "🅞", "✅","◉","()","|","[]","#"]
rmre = '|'.join(rmlist)



def clean_text(text, vocab=None):
    # Xóa định dạng HTML
    cleanr = re.compile(r'<[^>]+>|<.*?>|&nbsp;|&amp;|&lt;|&gt;|<STYLE>(.*?)<\/STYLE>|<style>(.*?)<\/style>|\u2026')

    # Xóa các ký tự đặc biệt, emoji, icon
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # dingbats
                               u"\U000024C2-\U0001F251" 
                               "]+", flags=re.UNICODE)

    # Xóa các hashtag
    hashtag_pattern = re.compile(r'#\S+')

    # Xóa các liên kết https
    #url_pattern = re.compile(r'http\S+')

    # Xóa các ký tự đặc biệt cụ thể
    special_characters = ['\u260e', '\u2026']

    # Áp dụng các mẫu để xóa phần không cần thiết
    text = re.sub(cleanr, ' ', text)
    text = re.sub(emoji_pattern, '', text)
    text = re.sub(hashtag_pattern, '', text)
    #text = re.sub(url_pattern, '', text)
    
    for char in special_characters:
        text = text.replace(char, '')

    # Xóa khoảng trắng thừa
    text = ' '.join(text.split())

    return text