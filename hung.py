from FactScoreLite import FactScore
import nltk
nltk.download('punkt')
import os
from dotenv import load_dotenv

load_dotenv()
ft = FactScore()
facts = [
    "trận đấu diễn ra vào 26 tháng 12"
    ]
knowledge_source = (
    "Trận bán kết lượt đi AFF Cup 2024 giữa đội tuyển Việt Nam và Singapore sẽ diễn ra vào ngày 26 tháng 12. HLV Kim Sang Sik bày tỏ sự tự tin về khả năng vượt qua áp lực của các cầu thủ, đặc biệt là Nguyễn Xuân Sơn, người đã có màn ra mắt ấn tượng với hai bàn thắng và hai kiến tạo trong trận đấu trước đó. Đội tuyển Việt Nam đã chuẩn bị kỹ lưỡng, nghiên cứu lối chơi của Singapore và xác định được những điểm yếu mà họ có thể khai thác. Mặc dù chỉ có khoảng 70 cổ động viên Việt Nam được vào sân, nhưng đội bóng vẫn nhận được sự ủng hộ từ xa của người hâm mộ. HLV Kim Sang Sik và các cầu thủ đều quyết tâm giành chiến thắng để tạo lợi thế cho trận lượt về."
)

a,b = ft.get_factscore(facts, [knowledge_source])
print(a,b) 

if b > 0:
    print("The facts are supported by the knowledge source.")
else:
    print("The facts are not supported by the knowledge source.")