from FactScoreLite import FactScore
import os
from dotenv import load_dotenv
load_dotenv()
def check_fact(facts, knowledge_source):
    ft = FactScore()
    a,b, decisions = ft.get_factscore([facts], [knowledge_source])
    print(decisions)
    if b > 0:
        return True
    else:
        return False

if __name__ == "__main__":
    facts = """
Ukraine gây bất ngờ cho Nga với cuộc tấn công mới ở Kursk
Kiev có “tin vui”
Cuộc tấn công của Ukraine vào khu vực Kursk của Nga hồi tháng 8 là một điều bất ngờ. Lực lượng vũ trang Kiev hiện đã mất nhiều vùng lãnh thổ rộng lớn, nhưng quân đội lại tiếp tục tấn công. Có thể củng cố vị thế của Ukraine trước lễ nhậm chức của Trump.
Theo thông tin từ Kiev, lực lượng vũ trang Ukraine đã phát động chiến dịch tấn công ở khu vực Kursk của Nga. Andriy Kovalenko, người đứng đầu Trung tâm chống thông tin sai lệch của Hội đồng Quốc phòng và An ninh Quốc gia Ukraina, viết trên Telegram: “Ở khu vực Kursk, người Nga rất lo lắng vì họ đã bị tấn công trên nhiều mặt trận và đây là một điều bất ngờ đối với họ. lực lượng phòng thủ được triển khai." Chánh văn phòng của Tổng thống Ukraine Zelensky, Andriy Yermak, nói: "Kursk, tin tốt, Nga đã nhận được những gì xứng đáng".
Cựu Thủy quân lục chiến Hoa Kỳ Rob Lee thuộc Viện Nghiên cứu Chính sách Đối ngoại đã chỉ ra một số kênh của Nga đưa tin về hoạt động tấn công của Ukraine bằng xe bọc thép gần Sujah. Thành phố này đã nằm dưới sự kiểm soát của Ukraine trong một thời gian dài.
Họ cho biết tác chiến điện tử của Kiev có hiệu quả chống lại máy bay không người lái của Nga và các đơn vị đã rà phá bom mìn chỉ sau một đêm. Theo Lee, một số kênh của Nga từ lâu đã cảnh báo về việc Ukraine triển khai quân và một cuộc tấn công có thể xảy ra trong khu vực.
Có thể tiến lên ở Tetkyno nữa?
Cũng có báo cáo về một cuộc tấn công theo hướng Tetkyno. Ở đó, về phía tây của mặt trận Kursk "lớn nhất", có một mặt trận nhỏ khác ở biên giới giữa Ukraine và Nga trên sông Seym. Khi bắt đầu cuộc tấn công Kursk cách đây vài tháng, Ukraine đã cố gắng tiến tới Tetkyno nhưng không thành công.
Các blogger quân sự Nga phản ứng khác nhau trước tin này. Trong khi một số trở nên lo lắng và cảnh báo về việc mất lãnh thổ, những người khác lại nói về việc giao tranh bình thường. Tuy nhiên, trên các kênh thân Ukraine, người ta đã bàn tán về những thành công. Các lực lượng vũ trang Ukraine vẫn chưa đưa ra bất kỳ tuyên bố chính thức nào.
Bộ Quốc phòng Nga viết trên Telegram rằng pháo binh và không quân Nga đã tấn công một cánh quân Ukraine trên đường tới thị trấn Berdin. Hai xe tăng, một xe dọn dẹp và bảy xe bọc thép bị phá hủy. Thông tin không thể được xác minh độc lập.
Tối hôm trước, Tổng thống Ukraine Zelensky đã nói về tổn thất nặng nề của Nga ở Kursk. Ông nói trong thông điệp video buổi tối: “Chỉ trong trận giao tranh hôm nay và hôm qua ở khu vực lân cận làng Makhnovka thuộc vùng Kursk, quân đội Nga đã mất một tiểu đoàn bộ binh gồm binh lính Triều Tiên và lính dù Nga”. Theo thông tin chính thức, một tiểu đoàn của lực lượng vũ trang Nga có quân số lên tới 500 người.
Những nỗ lực tấn công của Ukraine diễn ra khoảng hai tuần trước lễ nhậm chức tổng thống của Donald Trump tại Hoa Kỳ. Các cuộc đàm phán sau đó có thể diễn ra trong đó Ukraine muốn hành động với lập trường mạnh mẽ nhất có thể. Kyiv đã tuyên bố rằng đất nước này sẽ không tuân theo một nền hòa bình do Nga quyết định.
Xem tiếp các bản bản tin tại: https://bit.ly/3BM3J0d hoặc  https://bit.ly/40nZpOd 
YouTube 1: https://www.youtube.com/@thoibao-de 
YouTube 2: https://www.youtube.com/@ThoibaoNews 
FB: https://www.facebook.com/thoibao.de   
Xem thêm tin khác tại: https://thoibao.de . Nếu bị chặn tại VN, các bạn tải, cài App Opera miễn phí ( Link: https://bit.ly/4fo0DOQ ) rồi bật VPN của App này là đọc bài của #Thoibao.de #VOA #BBC #RFA... 
https://bit.ly/3BM3J0d"""
    knowledge_source = """
(Dân trí) - Một xe tăng Nga đã đẩy lùi hai xe tăng Ukraine trong cuộc giao tranh cận chiến hiếm hoi.
Trận đấu xe tăng được cho là đã diễn ra tại một ngôi làng gần thành phố Pokrovsk, khu định cư lớn nhất vẫn nằm dưới sự kiểm soát của Ukraine ở phía tây vùng Donetsk, miền Đông Ukraine. Trong những tuần gần đây, quân đội Nga đã giành quyền kiểm soát nhiều địa điểm ở phía nam và tây nam của thành phố này.
Khoảnh khắc xe tăng Nga - Ukraine cận chiến

Đoàn xe do một xe tăng dẫn đầu, với 3 xe khác dường như là xe chiến đấu bộ binh bọc thép hạng nặng (IFV).

Khi đến khu rừng, đoàn xe chạm trán với 2 xe tăng Ukraine cũng đang tiến dọc theo con đường.

Xe tăng Nga và xe tăng dẫn đầu của Ukraine khai hỏa, cả hai đều bắn trượt phát đầu tiên. Trong khi đó, các xe chiến đấu bộ binh tản ra và ẩn núp ở vùng ven của khu vực rừng rậm.

Sau đó, xe tăng Nga đã bắn nhiều phát vào xe tăng Ukraine, khiến xe này bốc cháy và không thể hoạt động.

Xe tăng thứ hai của Ukraine rút lui, trong khi một số máy bay không người lái góc nhìn thứ nhất (FPV) được triển khai để truy đuổi xe tăng này. Theo báo cáo, chiếc xe này cũng bị phá hủy.

Giao tranh trực tiếp giữa xe tăng và xe tăng là hoạt động rất hiếm trong cuộc xung đột giữa Nga và Ukraine, phần lớn do mật độ máy bay không người lái vô cùng cao được cả hai bên triển khai trên chiến trường.

Cả Moscow và Kiev đều sử dụng hiệu quả xe tăng làm hệ thống pháo binh cơ động, hoạt động từ các vị trí bắn được che chắn, trong khi các phiên bản bọc thép dày đóng vai trò là xe đột phá để dẫn đầu các cuộc tấn công vào các vị trí của đối phương.

Quân đội Nga đang thúc đẩy ngành công nghiệp quốc phòng để sản xuất vũ khí cũng như tuyển thêm quân. Các báo cáo gần đây chỉ ra rằng ngoài việc thay thế số quân bị mất trong các trận chiến, Nga cũng tăng cường sản xuất xe tăng.

Tình báo Anh cho biết việc Nga có thể duy trì tốc độ sản xuất xe tăng mỗi tháng cho phép Moscow duy trì nỗ lực tấn công Ukraine ở mức tương đương dù phải chịu tổn thất lớn.

Phương Tây nhiều lần nhận định Nga sắp cạn kiệt vũ khí và không có khả năng bù đắp do chịu hàng loạt lệnh trừng phạt. Tuy nhiên, trên thực tế, Nga vẫn liên tục đưa vũ khí mới ra chiến trường. Moscow cũng tuyên bố nâng cao năng lực sản xuất quốc phòng gấp nhiều lần, nhằm phục vụ cho cuộc chiến tiêu hao.

Việc Nga vẫn duy trì khả năng tấn công diễn ra trong bối cảnh viện trợ từ phương Tây cho Ukraine ngày càng nhỏ giọt, đặt Kiev vào thế khó để có thể đạt được mục tiêu giành lại lãnh thổ từ Moscow."""
    if check_fact(facts, knowledge_source):
        print("This is a fact")
    else:
        print("This is not a fact")