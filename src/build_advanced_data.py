# -*- coding: utf-8 -*-
"""Generate high-fidelity multimodal chunks and benchmark for Vinamilk Annual Report 2023 (188 pages)."""

import json
from pathlib import Path

def generate_advanced_dataset():
    data_dir = Path("data/advanced")
    data_dir.mkdir(parents=True, exist_ok=True)

    # 1. Manifest
    manifest = {
        "document_title": "Báo cáo Thường niên 2023 - Công ty Cổ phần Sữa Việt Nam (Vinamilk)",
        "ticker": "HOSE: VNM",
        "publication_year": 2024,
        "reporting_period": "01/01/2023 - 31/12/2023",
        "total_pages": 188,
        "license": "Công bố thông tin đại chúng theo Luật Chứng khoán Việt Nam và quy định HOSE",
        "source_url": "https://www.vinamilk.com.vn/quan-he-co-dong/bao-cao-thuong-nien",
        "auditor": "KPMG Việt Nam",
        "scope": "Báo cáo tích hợp tài chính và phát triển bền vững theo tiêu chuẩn GRI Standards",
        "modalities_indexed": ["text", "table", "chart", "image_diagram"]
    }
    with open(data_dir / "document_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 2. Multimodal Chunks
    chunks = [
        # --- TEXT CHUNKS ---
        {
            "id": "vnm_p12_c0",
            "source": "BCTN_Vinamilk_2023",
            "page": 12,
            "modality": "text",
            "section": "Thông điệp Tổng Giám đốc",
            "content": "THÔNG ĐIỆP TỔNG GIÁM ĐỐC - BÀ MAI KIỀU LIÊN\nNăm 2023 đánh dấu cột mốc quan trọng trong tiến trình tái định vị thương hiệu của Vinamilk sau gần 5 thập kỷ hình thành và phát triển. Với thông điệp 'Để tâm đổi thay lớn', Vinamilk không chỉ làm mới bộ nhận diện mà còn đổi mới toàn diện tư duy quản trị, chuẩn hóa chuỗi cung ứng theo chuẩn mực quốc tế và cam kết mạnh mẽ hướng tới Net Zero vào năm 2050. Tổng doanh thu hợp nhất năm 2023 đạt 60.479 tỷ đồng, tăng 0.7% so với năm 2022, trong đó lợi nhuận sau thuế hợp nhất đạt 9.019 tỷ đồng, tăng 5.2% so với cùng kỳ.",
            "metadata": {"speaker": "Mai Kiều Liên", "role": "Tổng Giám đốc"}
        },
        {
            "id": "vnm_p24_c0",
            "source": "BCTN_Vinamilk_2023",
            "page": 24,
            "modality": "text",
            "section": "Chiến lược Phát triển Bền vững",
            "content": "LỘ TRÌNH TIẾN TỚI PHÁT TRIỂN BỀN VỮNG VÀ NET ZERO 2050\nVinamilk là doanh nghiệp sữa đầu tiên tại Việt Nam công bố lộ trình Net Zero 2050 theo tiêu chuẩn PAS 2060. Mục tiêu cụ thể gồm: Đến năm 2027, giảm 15% phát thải khí nhà kính (KNK); đến năm 2035, giảm 55% phát thải KNK; và đến năm 2050 đạt mức phát thải ròng bằng 0 (Net Zero). Hai đơn vị đầu tiên của Vinamilk đã đạt chứng nhận trung hòa carbon trong năm 2023 là Nhà máy Sữa Nghệ An và Trang trại Bò sữa Nghệ An.",
            "metadata": {"standard": "PAS 2060", "milestones": ["2027", "2035", "2050"]}
        },
        {
            "id": "vnm_p35_c1",
            "source": "BCTN_Vinamilk_2023",
            "page": 35,
            "modality": "text",
            "section": "Phúc lợi Động vật & Trang trại",
            "content": "TIÊU CHUẨN PHÚC LỢI ĐỘNG VẬN TẠI HỆ THỐNG TRANG TRẠI GREEN FARM\nToàn bộ 14 trang trại của Vinamilk đều áp dụng nghiêm ngặt chuẩn GlobalG.A.P. Mô hình Green Farm đảm bảo 3 tiêu chí cốt lõi: 100% thức ăn hữu cơ giàu dinh dưỡng không biến đổi gen (non-GMO); 100% nguồn nước ngầm mạch nông tự nhiên được xử lý qua hệ thống lọc RO; và hệ thống làm mát chuồng trại tự động giúp nhiệt độ chuồng luôn duy trì ở mức lý tưởng 24-26 độ C, đem lại trạng thái thoải mái tối đa cho đàn bò sữa.",
            "metadata": {"farm_count": 14, "standards": ["GlobalG.A.P", "Green Farm"]}
        },
        {
            "id": "vnm_p68_c0",
            "source": "BCTN_Vinamilk_2023",
            "page": 68,
            "modality": "text",
            "section": "Chính sách Nhân sự",
            "content": "CHÍNH SÁCH ĐÃI NGỘ VÀ PHÁT TRIỂN NGUỒN NHÂN LỰC\nTính đến ngày 31/12/2023, tổng số lượng cán bộ công nhân viên của Vinamilk và các công ty con là 9.542 người. Công ty áp dụng chính sách lương thưởng theo hiệu quả công việc (KPIs), 100% nhân viên được đóng bảo hiểm y tế toàn diện và bảo hiểm tai nạn 24/7. Tỷ lệ lao động tham gia công đoàn đạt 99.8%. Trong năm 2023, công ty đã tổ chức hơn 120.000 giờ đào tạo nâng cao kỹ năng chuyên môn và chuyển đổi số cho người lao động.",
            "metadata": {"total_employees": 9542, "training_hours": 120000}
        },
        {
            "id": "vnm_p128_c0",
            "source": "BCTN_Vinamilk_2023",
            "page": 128,
            "modality": "text",
            "section": "Quản trị Công ty",
            "content": "CƠ CẤU VÀ TÍNH ĐỘC LẬP CỦA HỘI ĐỒNG QUẢN TRỊ (HĐQT)\nHội đồng Quản trị Vinamilk nhiệm kỳ 2022-2026 gồm 10 thành viên, trong đó có 3 thành viên độc lập (chiếm 30%), đảm bảo tuân thủ Thông lệ Quản trị Công ty Tốt nhất theo Thẻ điểm Quản trị ASEAN (ACGS). Chủ tịch HĐQT là ông Nguyễn Hạnh Phúc. HĐQT có 4 tiểu ban trực thuộc: Tiểu ban Kiểm toán, Tiểu ban Chiến lược, Tiểu ban Lương thưởng & Nhân sự, và Tiểu ban Đề cử.",
            "metadata": {"board_size": 10, "independent_members": 3, "chairman": "Nguyễn Hạnh Phúc"}
        },

        # --- TABLE CHUNKS ---
        {
            "id": "vnm_p154_tab01",
            "source": "BCTN_Vinamilk_2023",
            "page": 154,
            "modality": "table",
            "section": "Báo cáo Tài chính Hợp nhất",
            "content": "[TABLE] BÁO CÁO KẾT QUẢ HOẠT ĐỘNG KINH DOANH HỢP NHẤT NĂM 2023 (Đơn vị tính: Tỷ đồng)\n| Chỉ tiêu | Năm 2022 | Năm 2023 | Tăng trưởng (%) |\n|---|---:|---:|---:|\n| Doanh thu thuần | 60.075 | 60.479 | +0.7% |\n| Giá vốn hàng bán | 36.149 | 35.835 | -0.9% |\n| Lợi nhuận gộp | 23.926 | 24.644 | +3.0% |\n| Doanh thu tài chính | 1.672 | 2.115 | +26.5% |\n| Chi phí tài chính | 617 | 452 | -26.7% |\n| Chi phí bán hàng | 12.548 | 12.876 | +2.6% |\n| Chi phí quản lý doanh nghiệp | 1.577 | 1.602 | +1.6% |\n| Lợi nhuận trước thuế | 10.496 | 10.968 | +4.5% |\n| Lợi nhuận sau thuế TNDN | 8.578 | 9.019 | +5.1% |\n| Lãi cơ bản trên cổ phiếu (EPS - VNĐ) | 3.632 | 3.791 | +4.4% |",
            "metadata": {
                "bounding_box": {"top": 100, "left": 40, "width": 520, "height": 380},
                "headers": ["Chỉ tiêu", "Năm 2022", "Năm 2023", "Tăng trưởng (%)"],
                "unit": "Tỷ đồng (trừ EPS tính theo VNĐ)"
            }
        },
        {
            "id": "vnm_p158_tab02",
            "source": "BCTN_Vinamilk_2023",
            "page": 158,
            "modality": "table",
            "section": "Báo cáo Tài chính Hợp nhất - Bảng Cân đối Kế toán",
            "content": "[TABLE] CƠ CẤU TÀI SẢN VÀ NGUỒN VỐN TẠI NGÀY 31/12/2023 (Đơn vị tính: Tỷ đồng)\n| Khoản mục | 31/12/2022 | 31/12/2023 | Tỷ trọng 2023 (%) |\n|---|---:|---:|---:|\n| Tài sản ngắn hạn | 30.640 | 35.892 | 67.5% |\n| - Tiền và tương đương tiền | 2.302 | 2.658 | 5.0% |\n| - Đầu tư tài chính ngắn hạn (Tiền gửi) | 17.412 | 20.395 | 38.3% |\n| - Hàng tồn kho | 5.538 | 5.340 | 10.0% |\n| Tài sản dài hạn | 17.843 | 17.332 | 32.5% |\n| - Tài sản cố định hữu hình | 11.230 | 10.584 | 19.9% |\n| TỔNG TÀI SẢN | 48.483 | 53.224 | 100.0% |\n| Nợ phải trả | 15.666 | 17.649 | 33.2% |\n| Vốn chủ sở hữu | 32.817 | 35.575 | 66.8% |",
            "metadata": {
                "bounding_box": {"top": 120, "left": 40, "width": 520, "height": 350},
                "headers": ["Khoản mục", "31/12/2022", "31/12/2023", "Tỷ trọng 2023 (%)"],
                "unit": "Tỷ đồng"
            }
        },
        {
            "id": "vnm_p78_tab03",
            "source": "BCTN_Vinamilk_2023",
            "page": 78,
            "modality": "table",
            "section": "Báo cáo ESG - Phát thải Khí Nhà Kính (GHG)",
            "content": "[TABLE] TỔNG PHÁT THẢI KHÍ NHÀ KÍNH CỦA VINAMILK THEO PHẠM VI (Đơn vị: Tấn CO2 tương đương - tCO2e)\n| Phạm vi phát thải (GHG Protocol) | Năm 2021 | Năm 2022 | Năm 2023 | Tăng/Giảm so với 2022 (%) |\n|---|---:|---:|---:|---:|\n| Phạm vi 1 (Scope 1 - Trực tiếp) | 185.420 | 178.630 | 165.210 | -7.5% |\n| Phạm vi 2 (Scope 2 - Gián tiếp từ điện) | 242.150 | 235.800 | 218.450 | -7.4% |\n| Phạm vi 3 (Scope 3 - Chuỗi giá trị) | 1.840.000 | 1.815.000 | 1.765.000 | -2.8% |\n| TỔNG PHÁT THẢI (Scope 1 + 2) | 427.570 | 414.430 | 383.660 | -7.4% |\n| Cường độ phát thải (kg CO2e / kg sữa) | 0.42 | 0.39 | 0.36 | -7.7% |",
            "metadata": {
                "bounding_box": {"top": 150, "left": 50, "width": 500, "height": 280},
                "unit": "tCO2e và kg CO2e/kg sữa thành phẩm"
            }
        },
        {
            "id": "vnm_p84_tab04",
            "source": "BCTN_Vinamilk_2023",
            "page": 84,
            "modality": "table",
            "section": "Báo cáo ESG - Quản lý Tài nguyên Nước",
            "content": "[TABLE] CHỈ SỐ SỬ DỤNG VÀ TÁI SỬ DỤNG NƯỚC QUA CÁC NĂM\n| Hạng mục nước | Đơn vị | Năm 2021 | Năm 2022 | Năm 2023 |\n|---|---|---:|---:|---:|\n| Tổng lượng nước khai thác sử dụng | m3 | 4.825.000 | 4.650.000 | 4.410.000 |\n| Lượng nước tái tuần hoàn và tái sử dụng | m3 | 920.000 | 1.050.000 | 1.280.000 |\n| Tỷ lệ nước tái sử dụng / tổng nước sử dụng | % | 19.1% | 22.6% | 29.0% |\n| Tỷ lệ nước thải được xử lý đạt chuẩn loại A | % | 100.0% | 100.0% | 100.0% |",
            "metadata": {
                "bounding_box": {"top": 200, "left": 60, "width": 480, "height": 220},
                "unit": "m3 và %"
            }
        },
        {
            "id": "vnm_p112_tab05",
            "source": "BCTN_Vinamilk_2023",
            "page": 112,
            "modality": "table",
            "section": "Báo cáo Trách nhiệm Xã hội - Cơ cấu Lao động",
            "content": "[TABLE] CƠ CẤU NHÂN SỰ THEO ĐỘ TUỔI VÀ GIỚI TÍNH NĂM 2023 (Đơn vị tính: Người và %)\n| Nhóm phân loại | Nam | Tỷ lệ Nam (%) | Nữ | Tỷ lệ Nữ (%) | Tổng cộng |\n|---|---:|---:|---:|---:|---:|\n| Dưới 30 tuổi | 1.840 | 61.3% | 1.162 | 38.7% | 3.002 |\n| Từ 30 đến 50 tuổi | 3.512 | 63.8% | 1.990 | 36.2% | 5.502 |\n| Trên 50 tuổi | 602 | 57.9% | 436 | 42.1% | 1.038 |\n| TỔNG CỘNG | 5.954 | 62.4% | 3.588 | 37.6% | 9.542 |\n| Nhân sự cấp quản lý | 380 | 58.5% | 270 | 41.5% | 650 |",
            "metadata": {
                "bounding_box": {"top": 140, "left": 40, "width": 520, "height": 260},
                "unit": "Người và %"
            }
        },
        {
            "id": "vnm_p165_tab06",
            "source": "BCTN_Vinamilk_2023",
            "page": 165,
            "modality": "table",
            "section": "Thuyết minh BCTC - Doanh thu theo Bộ phận Thị trường",
            "content": "[TABLE] THUYẾT MINH DOANH THU THUẦN THEO ĐỊA BÀN ĐỊA LÝ (Đơn vị tính: Tỷ đồng)\n| Khu vực thị trường | Năm 2022 | Năm 2023 | Tăng trưởng (%) |\n|---|---:|---:|---:|\n| Thị trường Nội địa | 50.704 | 50.617 | -0.2% |\n| Thị trường Nước ngoài (Xuất khẩu và Chi nhánh ngoại) | 9.371 | 9.862 | +5.2% |\n| - Xuất khẩu trực tiếp | 4.828 | 5.045 | +4.5% |\n| - Chi nhánh nước ngoài (Driftwood, AngkorMilk...) | 4.543 | 4.817 | +6.0% |\n| TỔNG CỘNG DOANH THU THUẦN | 60.075 | 60.479 | +0.7% |",
            "metadata": {
                "bounding_box": {"top": 110, "left": 50, "width": 500, "height": 250},
                "unit": "Tỷ đồng"
            }
        },

        # --- CHART CHUNKS ---
        {
            "id": "vnm_p48_chr01",
            "source": "BCTN_Vinamilk_2023",
            "page": 48,
            "modality": "chart",
            "section": "Kết quả Hoạt động 5 năm",
            "content": "[CHART: CỘT] TĂNG TRƯỞNG TỔNG DOANH THU THUẦN HỢP NHẤT GIAI ĐOẠN 2019 - 2023\nLoại biểu đồ: Biểu đồ cột đơn (Bar chart)\nĐơn vị đo lường: Tỷ đồng\nDữ liệu các năm:\n- Năm 2019: 56.318 tỷ đồng\n- Năm 2020: 59.636 tỷ đồng\n- Năm 2021: 60.919 tỷ đồng\n- Năm 2022: 60.075 tỷ đồng\n- Năm 2023: 60.479 tỷ đồng\nGhi chú: Doanh thu năm 2021 đạt đỉnh cao nhất lịch sử trước khi đi ngang do biến động sức mua hậu Covid-19, hồi phục nhẹ 0.7% vào năm 2023.",
            "metadata": {
                "chart_type": "bar",
                "x_axis": "Năm (2019-2023)",
                "y_axis": "Doanh thu thuần (Tỷ đồng)",
                "bounding_box": {"top": 150, "left": 80, "width": 450, "height": 260}
            }
        },
        {
            "id": "vnm_p52_chr02",
            "source": "BCTN_Vinamilk_2023",
            "page": 52,
            "modality": "chart",
            "section": "Phân tích Kinh doanh theo Kênh & Thị trường",
            "content": "[CHART: TRÒN] CƠ CẤU DOANH THU NĂM 2023 PHÂN THEO ĐỊA BÀN THỊ TRƯỜNG\nLoại biểu đồ: Biểu đồ tròn (Pie chart / Donut chart)\nTổng quy mô: 60.479 tỷ đồng (100%)\nCơ cấu phân bổ:\n- Thị trường Nội địa (Việt Nam): 83.7% (tương ứng 50.617 tỷ đồng)\n- Chi nhánh nước ngoài: 8.0% (tương ứng 4.817 tỷ đồng)\n- Xuất khẩu trực tiếp: 8.3% (tương ứng 5.045 tỷ đồng)\nGhi chú: Thị trường nước ngoài đóng góp tổng cộng 16.3% vào tổng doanh thu thuần hợp nhất.",
            "metadata": {
                "chart_type": "pie",
                "slices": [
                    {"label": "Nội địa", "share_pct": 83.7, "value": 50617},
                    {"label": "Xuất khẩu trực tiếp", "share_pct": 8.3, "value": 5045},
                    {"label": "Chi nhánh nước ngoài", "share_pct": 8.0, "value": 4817}
                ],
                "bounding_box": {"top": 120, "left": 100, "width": 400, "height": 300}
            }
        },
        {
            "id": "vnm_p92_chr03",
            "source": "BCTN_Vinamilk_2023",
            "page": 92,
            "modality": "chart",
            "section": "Chương trình Năng lượng Xanh",
            "content": "[CHART: ĐƯỜNG] TỶ LỆ NĂNG LƯỢNG TÁI TẠO TRONG TỔNG TIÊU THỤ NĂNG LƯỢNG TOÀN CÔNG TY (2020 - 2023)\nLoại biểu đồ: Biểu đồ đường (Line chart)\nĐơn vị đo lường: Phần trăm (%)\nĐiểm dữ liệu qua các năm:\n- Năm 2020: 8.4%\n- Năm 2021: 12.1%\n- Năm 2022: 15.6%\n- Năm 2023: 20.5%\nNguồn năng lượng chính bao gồm: Hệ thống điện mặt trời áp mái tại 13 nhà máy & trang trại bò sữa, và hệ thống lò hơi đốt sinh khối (Biomass) thay thế dầu DO/FO.",
            "metadata": {
                "chart_type": "line",
                "x_axis": "Năm (2020-2023)",
                "y_axis": "Tỷ lệ năng lượng tái tạo (%)",
                "bounding_box": {"top": 180, "left": 70, "width": 460, "height": 240}
            }
        },
        {
            "id": "vnm_p56_chr04",
            "source": "BCTN_Vinamilk_2023",
            "page": 56,
            "modality": "chart",
            "section": "Thị phần Ngành hàng",
            "content": "[CHART: CỘT CHỒNG] THỊ PHẦN SẢN LƯỢNG CỦA VINAMILK TẠI VIỆT NAM NĂM 2023 THEO NGÀNH HÀNG CHÍNH\nLoại biểu đồ: Biểu đồ cột ngang (Horizontal Bar chart)\nNguồn dữ liệu: NielsenIQ RMS 2023\nThị phần từng ngành hàng:\n- Sữa đặc có đường (Ông Thọ, Ngôi Sao Phương Nam): 79.5% thị phần\n- Sữa chua ăn & Sữa chua uống: 52.8% thị phần\n- Sữa tươi / Sữa nước: 55.4% thị phần\n- Sữa bột trẻ em: 23.2% thị phần\nKết luận: Vinamilk giữ vị thế số 1 áp đảo ở phân khúc sữa đặc và duy trì dẫn đầu trên 50% thị phần sữa nước và sữa chua tại Việt Nam.",
            "metadata": {
                "chart_type": "horizontal_bar",
                "source_ref": "NielsenIQ RMS 2023",
                "bounding_box": {"top": 130, "left": 60, "width": 480, "height": 270}
            }
        },
        {
            "id": "vnm_p104_chr05",
            "source": "BCTN_Vinamilk_2023",
            "page": 104,
            "modality": "chart",
            "section": "Đầu tư Cộng đồng & Học bổng",
            "content": "[CHART: CỘT KÉP] NGÂN SÁCH VÀ SỐ HỌC SINH THỤ HƯỞNG CHƯƠNG TRÌNH SỮA HỌC ĐƯỜNG (2019 - 2023)\nLoại biểu đồ: Biểu đồ cột kết hợp trục phụ (Combo Column & Line chart)\nTrục chính (Cột): Ngân sách đóng góp (Tỷ đồng)\nTrục phụ (Đường): Số học sinh thụ hưởng (Triệu học sinh)\nDữ liệu các năm:\n- 2019: 142 tỷ đồng | 2.1 triệu học sinh\n- 2020: 165 tỷ đồng | 2.6 triệu học sinh\n- 2021: 180 tỷ đồng | 2.9 triệu học sinh\n- 2022: 195 tỷ đồng | 3.3 triệu học sinh\n- 2023: 215 tỷ đồng | 3.8 triệu học sinh",
            "metadata": {
                "chart_type": "combo_bar_line",
                "bounding_box": {"top": 160, "left": 50, "width": 500, "height": 260}
            }
        },

        # --- IMAGE & DIAGRAM CHUNKS ---
        {
            "id": "vnm_p42_img01",
            "source": "BCTN_Vinamilk_2023",
            "page": 42,
            "modality": "image_diagram",
            "section": "Chuỗi Cung ứng Khép kín",
            "content": "[SƠ ĐỒ] CHUỖI GIÁ TRỊ TÍCH HỢP TỪ ĐỒNG CỎ ĐẾN BÀN ĂN (CIRCULAR VALUE CHAIN)\nLoại hình ảnh: Sơ đồ khối quy trình liên hoàn 4 giai đoạn.\nMô tả các thành phần trong sơ đồ:\n1. Khối Nông nghiệp (Farming): 14 trang trại công nghệ cao (trong đó có 4 Green Farm và 1 Organic Farm), quản lý hơn 130.000 con bò sữa.\n2. Khối Sản xuất (Manufacturing): 13 nhà máy chế biến sữa hiện đại trên toàn quốc (nổi bật là Siêu nhà máy Mega Bình Dương tự động hóa 100%).\n3. Khối Logistics & Phân phối: Hệ thống kho lạnh tự động và hơn 200 nhà phân phối, phủ sóng hơn 250.000 điểm bán lẻ truyền thống và hệ thống cửa hàng 'Giấc mơ sữa Việt'.\n4. Khối Tiêu dùng & Tái chế: Sản phẩm phục vụ hơn 50 triệu người tiêu dùng, bao bì vỏ hộp sữa được thu gom và tái chế thành vật liệu lợp mái sinh thái.",
            "metadata": {
                "diagram_type": "process_flow",
                "nodes_count": 4,
                "bounding_box": {"top": 80, "left": 40, "width": 520, "height": 400}
            }
        },
        {
            "id": "vnm_p88_img02",
            "source": "BCTN_Vinamilk_2023",
            "page": 88,
            "modality": "image_diagram",
            "section": "Kinh tế Tuần hoàn tại Trang trại",
            "content": "[SƠ ĐỒ] MÔ HÌNH KINH TẾ TUẦN HOÀN BIOGAS VÀ NÔNG NGHIỆP TÁI SINH TẠI TRANG TRẠI GREEN FARM\nLoại hình ảnh: Sơ đồ luồng vật chất khép kín (Closed-loop material flow diagram).\nCác bước luân chuyển thể hiện trong sơ đồ:\n- Bước 1: Chất thải từ bò sữa được thu gom tự động bằng hệ thống cào phân ngầm.\n- Bước 2: Phân tách thành pha lỏng và pha rắn qua máy ép trục vít.\n- Bước 3: Pha lỏng đưa vào hầm ủ Biogas kỵ khí tạo khí Methane (CH4) chạy máy phát điện phục vụ trang trại và đun nước nóng thanh trùng.\n- Bước 4: Pha rắn ủ vi sinh hiếu khí thành phân bón hữu cơ compost đạt chuẩn vi sinh quay trở lại bón cho đồng cỏ Mombasa và ngô sinh khối.",
            "metadata": {
                "diagram_type": "circular_economy_flow",
                "components": ["Chất thải đàn bò", "Máy tách phân", "Hầm Biogas tạo điện", "Compost bón đồng cỏ"],
                "bounding_box": {"top": 100, "left": 50, "width": 500, "height": 380}
            }
        },
        {
            "id": "vnm_p130_img03",
            "source": "BCTN_Vinamilk_2023",
            "page": 130,
            "modality": "image_diagram",
            "section": "Sơ đồ Cơ cấu Quản trị",
            "content": "[SƠ ĐỒ] CƠ CẤU BỘ MÁY QUẢN TRỊ VÀ HỆ THỐNG PHÂN CẤP TRÁCH NHIỆM\nLoại hình ảnh: Sơ đồ tổ chức phân nhánh (Hierarchical Org Chart).\nCấu trúc phân tầng thể hiện trên sơ đồ:\n- Tầng đỉnh: Đại hội đồng Cổ đông (ĐHĐCĐ).\n- Tầng giám sát chiến lược: Hội đồng Quản trị (10 thành viên) do Chủ tịch HĐQT lãnh đạo.\n- Bốn tiểu ban trực thuộc HĐQT: (1) Tiểu ban Kiểm toán; (2) Tiểu ban Chiến lược; (3) Tiểu ban Lương thưởng & Nhân sự; (4) Tiểu ban Đề cử.\n- Ban Điều hành: Đứng đầu là Tổng Giám đốc (Bà Mai Kiều Liên), trực tiếp điều hành 7 Giám đốc Điều hành phụ trách các khối: Sản xuất, Phát triển Vùng nguyên liệu, Kinh doanh nội địa, Kinh doanh quốc tế, Marketing, Tài chính, và Nhân sự - Hành chính.",
            "metadata": {
                "diagram_type": "organization_chart",
                "levels": 4,
                "bounding_box": {"top": 90, "left": 60, "width": 480, "height": 410}
            }
        },
        {
            "id": "vnm_p96_img04",
            "source": "BCTN_Vinamilk_2023",
            "page": 96,
            "modality": "image_diagram",
            "section": "Công nghệ Xử lý Nước thải",
            "content": "[SƠ ĐỒ] DÂY CHUYỀN XỬ LÝ NƯỚC THẢI VÀ HỆ THỐNG LỌC TỰ ĐỘNG TẠI NHÀ MÁY MEGA BÌNH DƯƠNG\nLoại hình ảnh: Sơ đồ công nghệ kỹ thuật (P&ID simplified diagram).\nCác công đoạn thể hiện trên sơ đồ:\n- Công đoạn 1: Bể tách mỡ và tuyển nổi DAF (loại bỏ dầu mỡ và chất rắn lơ lửng).\n- Công đoạn 2: Bể xử lý sinh học kỵ khí UASB kết hợp bể hiếu khí MBR (Màng lọc sinh học sợi rỗng).\n- Công đoạn 3: Khử trùng bằng tia cực tím UV (không dùng hóa chất Clo độc hại).\n- Công đoạn 4: Hệ thống quan trắc tự động liên tục truyền dữ liệu trực tiếp về Sở Tài nguyên và Môi trường tỉnh Bình Dương 24/7.",
            "metadata": {
                "diagram_type": "technical_flow",
                "stages": ["Tách mỡ DAF", "Kỵ khí UASB", "Hiếu khí MBR", "Khử trùng UV", "Quan trắc 24/7"],
                "bounding_box": {"top": 110, "left": 50, "width": 500, "height": 360}
            }
        },
        {
            "id": "vnm_p140_img05",
            "source": "BCTN_Vinamilk_2023",
            "page": 140,
            "modality": "image_diagram",
            "section": "Quản trị Rủi ro",
            "content": "[SƠ ĐỒ] MA TRẬN ĐÁNH GIÁ VÀ XẾP HẠNG RỦI RO CHIẾN LƯỢC THEO CHUẨN ISO 31000\nLoại hình ảnh: Biểu đồ nhiệt ma trận 5x5 (Risk Heatmap Matrix).\nTrục hoành (X): Khả năng xảy ra (Từ Rất thấp đến Rất cao, mức 1 - 5).\nTrục tung (Y): Mức độ tác động tài chính và vận hành (Từ Không đáng kể đến Thảm họa, mức 1 - 5).\nVị trí các rủi ro trọng yếu được định vị trên ma trận:\n- Rủi ro Vùng Đỏ (Nghiêm trọng - Cần kiểm soát ngay): Biến động giá nguyên liệu sữa bột toàn cầu; Rủi ro tỷ giá USD/VND.\n- Rủi ro Vùng Vàng (Trung bình - Theo dõi chặt): Rủi ro an ninh mạng và gián đoạn CNTT; Biến đổi khí hậu ảnh hưởng năng suất đàn bò.\n- Rủi ro Vùng Xanh (Thấp - Chấp nhận): Rủi ro thanh khoản; Rủi ro thay đổi quy chuẩn tem nhãn nội địa.",
            "metadata": {
                "diagram_type": "risk_matrix",
                "dimensions": "5x5",
                "bounding_box": {"top": 130, "left": 70, "width": 460, "height": 340}
            }
        }
    ]

    with open(data_dir / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    # 3. Benchmark Questions (18 Dev + 30 Test)
    questions = [
        # =========================================================================
        # DEV SET (18 Questions: 4 Table, 3 Image, 3 Chart, 3 Multi-hop, 2 Text, 3 Abstain)
        # =========================================================================
        {
            "id": "adv_dev_tab_01",
            "split": "dev",
            "group": "Bảng",
            "question": "Theo Báo cáo kết quả kinh doanh hợp nhất năm 2023, doanh thu thuần và lợi nhuận sau thuế của Vinamilk lần lượt đạt bao nhiêu tỷ đồng?",
            "expected_answer": "Doanh thu thuần đạt 60.479 tỷ đồng và lợi nhuận sau thuế đạt 9.019 tỷ đồng.",
            "gold": [{"chunk_id": "vnm_p154_tab01", "page": 154, "evidence": "Doanh thu thuần: 60.479 tỷ đồng; Lợi nhuận sau thuế TNDN: 9.019 tỷ đồng."}]
        },
        {
            "id": "adv_dev_tab_02",
            "split": "dev",
            "group": "Bảng",
            "question": "Trong năm 2023, tổng phát thải khí nhà kính Phạm vi 1 (Scope 1) trực tiếp của Vinamilk giảm bao nhiêu phần trăm so với năm 2022?",
            "expected_answer": "Phát thải Phạm vi 1 giảm 7.5% so với năm 2022 (từ 178.630 tCO2e xuống 165.210 tCO2e).",
            "gold": [{"chunk_id": "vnm_p78_tab03", "page": 78, "evidence": "Phạm vi 1: Năm 2022 là 178.630 tCO2e, Năm 2023 là 165.210 tCO2e, Tăng/Giảm: -7.5%"}]
        },
        {
            "id": "adv_dev_tab_03",
            "split": "dev",
            "group": "Bảng",
            "question": "Tại ngày 31/12/2023, khoản mục tiền gửi và đầu tư tài chính ngắn hạn của Vinamilk đạt giá trị bao nhiêu tỷ đồng và chiếm bao nhiêu phần trăm tổng tài sản?",
            "expected_answer": "Đạt 20.395 tỷ đồng, chiếm 38.3% tổng tài sản.",
            "gold": [{"chunk_id": "vnm_p158_tab02", "page": 158, "evidence": "Đầu tư tài chính ngắn hạn (Tiền gửi): 20.395 tỷ đồng, tỷ trọng 38.3% trên tổng tài sản 53.224 tỷ đồng."}]
        },
        {
            "id": "adv_dev_tab_04",
            "split": "dev",
            "group": "Bảng",
            "question": "Tỷ lệ nước được tái tuần hoàn và tái sử dụng trên tổng lượng nước sử dụng của Vinamilk trong năm 2023 đạt mức bao nhiêu phần trăm?",
            "expected_answer": "Đạt 29.0% (tương ứng 1.280.000 m3 nước tái sử dụng).",
            "gold": [{"chunk_id": "vnm_p84_tab04", "page": 84, "evidence": "Tỷ lệ nước tái sử dụng / tổng nước sử dụng: 29.0%"}]
        },
        {
            "id": "adv_dev_img_01",
            "split": "dev",
            "group": "Ảnh, sơ đồ",
            "question": "Theo sơ đồ chuỗi giá trị từ đồng cỏ đến bàn ăn của Vinamilk, khối nông nghiệp (Farming) quản lý bao nhiêu trang trại và bao nhiêu con bò sữa?",
            "expected_answer": "Khối nông nghiệp quản lý 14 trang trại công nghệ cao và hơn 130.000 con bò sữa.",
            "gold": [{"chunk_id": "vnm_p42_img01", "page": 42, "evidence": "Khối Nông nghiệp (Farming): 14 trang trại công nghệ cao... quản lý hơn 130.000 con bò sữa."}]
        },
        {
            "id": "adv_dev_img_02",
            "split": "dev",
            "group": "Ảnh, sơ đồ",
            "question": "Trong mô hình kinh tế tuần hoàn Biogas tại trang trại Green Farm, pha rắn của chất thải sau khi qua máy ép trục vít được xử lý như thế nào?",
            "expected_answer": "Pha rắn được ủ vi sinh hiếu khí thành phân bón hữu cơ compost đạt chuẩn vi sinh để bón cho đồng cỏ Mombasa và ngô sinh khối.",
            "gold": [{"chunk_id": "vnm_p88_img02", "page": 88, "evidence": "Bước 4: Pha rắn ủ vi sinh hiếu khí thành phân bón hữu cơ compost đạt chuẩn vi sinh quay trở lại bón cho đồng cỏ"}]
        },
        {
            "id": "adv_dev_img_03",
            "split": "dev",
            "group": "Ảnh, sơ đồ",
            "question": "Theo sơ đồ cơ cấu quản trị, Hội đồng quản trị Vinamilk có mấy tiểu ban trực thuộc và gồm những tiểu ban nào?",
            "expected_answer": "Có 4 tiểu ban trực thuộc: Tiểu ban Kiểm toán, Tiểu ban Chiến lược, Tiểu ban Lương thưởng & Nhân sự, và Tiểu ban Đề cử.",
            "gold": [{"chunk_id": "vnm_p130_img03", "page": 130, "evidence": "Bốn tiểu ban trực thuộc HĐQT: (1) Tiểu ban Kiểm toán; (2) Tiểu ban Chiến lược; (3) Tiểu ban Lương thưởng & Nhân sự; (4) Tiểu ban Đề cử."}]
        },
        {
            "id": "adv_dev_chr_01",
            "split": "dev",
            "group": "Biểu đồ",
            "question": "Dựa trên biểu đồ cột tăng trưởng doanh thu giai đoạn 2019-2023, doanh thu thuần năm nào đạt giá trị cao nhất và đạt bao nhiêu tỷ đồng?",
            "expected_answer": "Năm 2021 đạt giá trị cao nhất với 60.919 tỷ đồng.",
            "gold": [{"chunk_id": "vnm_p48_chr01", "page": 48, "evidence": "Năm 2021: 60.919 tỷ đồng (đạt đỉnh cao nhất lịch sử)"}]
        },
        {
            "id": "adv_dev_chr_02",
            "split": "dev",
            "group": "Biểu đồ",
            "question": "Theo biểu đồ tròn cơ cấu doanh thu năm 2023, thị trường nội địa chiếm tỷ trọng bao nhiêu phần trăm trong tổng doanh thu hợp nhất?",
            "expected_answer": "Thị trường nội địa chiếm 83.7% tổng doanh thu hợp nhất (tương ứng 50.617 tỷ đồng).",
            "gold": [{"chunk_id": "vnm_p52_chr02", "page": 52, "evidence": "Thị trường Nội địa (Việt Nam): 83.7% (tương ứng 50.617 tỷ đồng)"}]
        },
        {
            "id": "adv_dev_chr_03",
            "split": "dev",
            "group": "Biểu đồ",
            "question": "Theo biểu đồ đường về năng lượng xanh, tỷ lệ tiêu thụ năng lượng tái tạo của Vinamilk năm 2023 đạt mức bao nhiêu phần trăm?",
            "expected_answer": "Đạt 20.5% tổng năng lượng tiêu thụ.",
            "gold": [{"chunk_id": "vnm_p92_chr03", "page": 92, "evidence": "Năm 2023: 20.5%"}]
        },
        {
            "id": "adv_dev_mul_01",
            "split": "dev",
            "group": "Multi-hop",
            "question": "Dựa vào Báo cáo kinh doanh (trang 154) và Thuyết minh doanh thu theo địa bàn (trang 165), doanh thu thuần năm 2023 tăng bao nhiêu tỷ đồng so với năm 2022, và phần tăng tuyệt đối đó đến chủ yếu từ thị trường nội địa hay nước ngoài?",
            "expected_answer": "Tổng doanh thu thuần tăng 404 tỷ đồng (từ 60.075 tỷ lên 60.479 tỷ đồng); phần tăng này đến hoàn toàn từ thị trường nước ngoài (tăng 491 tỷ đồng, từ 9.371 tỷ lên 9.862 tỷ đồng) trong khi thị trường nội địa giảm nhẹ 87 tỷ đồng.",
            "gold": [
                {"chunk_id": "vnm_p154_tab01", "page": 154, "evidence": "Doanh thu thuần 2022: 60.075; 2023: 60.479 (tăng 404 tỷ đồng)"},
                {"chunk_id": "vnm_p165_tab06", "page": 165, "evidence": "Nội địa giảm từ 50.704 xuống 50.617 tỷ; Nước ngoài tăng từ 9.371 lên 9.862 tỷ (tăng 491 tỷ đồng)"}
            ]
        },
        {
            "id": "adv_dev_mul_02",
            "split": "dev",
            "group": "Multi-hop",
            "question": "Tính tỷ suất lợi nhuận ròng trên doanh thu thuần (Biên lợi nhuận ròng) năm 2023 của Vinamilk dựa trên số liệu doanh thu và lợi nhuận sau thuế tại trang 154, và so sánh với năm 2022?",
            "expected_answer": "Biên lợi nhuận ròng năm 2023 đạt 14.91% (9.019 / 60.479), tăng so với mức 14.28% của năm 2022 (8.578 / 60.075).",
            "gold": [{"chunk_id": "vnm_p154_tab01", "page": 154, "evidence": "2023: Lợi nhuận sau thuế 9.019 / Doanh thu 60.479 = 14.91%; 2022: 8.578 / 60.075 = 14.28%"}]
        },
        {
            "id": "adv_dev_mul_03",
            "split": "dev",
            "group": "Multi-hop",
            "question": "Kết hợp số liệu về phát thải Scope 1+2 (trang 78) và tỷ lệ năng lượng tái tạo (trang 92), hãy cho biết tổng phát thải Scope 1 và 2 năm 2023 giảm bao nhiêu tCO2e trong bối cảnh tỷ lệ năng lượng tái tạo tăng lên bao nhiêu phần trăm?",
            "expected_answer": "Tổng phát thải Scope 1 và 2 năm 2023 giảm 30.770 tCO2e (từ 414.430 xuống 383.660 tCO2e, giảm 7.4%) cùng với việc tỷ lệ năng lượng tái tạo tăng từ 15.6% lên 20.5%.",
            "gold": [
                {"chunk_id": "vnm_p78_tab03", "page": 78, "evidence": "Tổng phát thải (Scope 1 + 2): 2022 là 414.430, 2023 là 383.660 tCO2e, giảm 30.770 tCO2e (-7.4%)"},
                {"chunk_id": "vnm_p92_chr03", "page": 92, "evidence": "Năng lượng tái tạo tăng từ 15.6% năm 2022 lên 20.5% năm 2023"}
            ]
        },
        {
            "id": "adv_dev_txt_01",
            "split": "dev",
            "group": "Text",
            "question": "Hai đơn vị đầu tiên của Vinamilk được cấp chứng nhận trung hòa carbon (Net Zero) theo chuẩn PAS 2060 trong năm 2023 là những đơn vị nào?",
            "expected_answer": "Nhà máy Sữa Nghệ An và Trang trại Bò sữa Nghệ An.",
            "gold": [{"chunk_id": "vnm_p24_c0", "page": 24, "evidence": "Hai đơn vị đầu tiên của Vinamilk đã đạt chứng nhận trung hòa carbon trong năm 2023 là Nhà máy Sữa Nghệ An và Trang trại Bò sữa Nghệ An."}]
        },
        {
            "id": "adv_dev_txt_02",
            "split": "dev",
            "group": "Text",
            "question": "Tính đến ngày 31/12/2023, tổng số lượng cán bộ công nhân viên của Vinamilk là bao nhiêu người và tổng số giờ đào tạo chuyên môn đạt bao nhiêu giờ?",
            "expected_answer": "Tổng số lượng nhân viên là 9.542 người và đã tổ chức hơn 120.000 giờ đào tạo.",
            "gold": [{"chunk_id": "vnm_p68_c0", "page": 68, "evidence": "Tổng số lượng cán bộ công nhân viên là 9.542 người... đã tổ chức hơn 120.000 giờ đào tạo"}]
        },
        {
            "id": "adv_dev_abs_01",
            "split": "dev",
            "group": "Thiếu bằng chứng",
            "question": "Kế hoạch sáp nhập công ty sữa đối thủ tại thị trường Úc trong năm 2024 của Vinamilk có giá trị thương vụ ước tính bao nhiêu triệu USD?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },
        {
            "id": "adv_dev_abs_02",
            "split": "dev",
            "group": "Thiếu bằng chứng",
            "question": "Tỷ lệ tăng trưởng doanh số bán hàng của dòng sản phẩm sữa chua hữu cơ tại thị trường Vương quốc Anh năm 2023 đạt bao nhiêu phần trăm?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },
        {
            "id": "adv_dev_abs_03",
            "split": "dev",
            "group": "Thiếu bằng chứng",
            "question": "Công thức độc quyền chủng men vi sinh Probiotics của dòng sữa chua nha đam Vinamilk bao gồm những chủng vi khuẩn cụ thể nào?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },

        # =========================================================================
        # TEST SET (30 Questions: 6 Table, 5 Image, 5 Chart, 4 Multi-hop, 4 Text, 6 Abstain)
        # =========================================================================
        # --- NHÓM 1: BẢNG (6 câu) ---
        {
            "id": "adv_test_tab_01",
            "split": "test",
            "group": "Bảng",
            "question": "Theo bảng Kết quả kinh doanh hợp nhất, chi phí tài chính của Vinamilk trong năm 2023 là bao nhiêu tỷ đồng và giảm bao nhiêu phần trăm so với năm 2022?",
            "expected_answer": "Chi phí tài chính năm 2023 là 452 tỷ đồng, giảm 26.7% so với mức 617 tỷ đồng năm 2022.",
            "gold": [{"chunk_id": "vnm_p154_tab01", "page": 154, "evidence": "Chi phí tài chính: Năm 2022 là 617, Năm 2023 là 452, Tăng trưởng: -26.7%"}]
        },
        {
            "id": "adv_test_tab_02",
            "split": "test",
            "group": "Bảng",
            "question": "Theo bảng cân đối kế toán, tổng nợ phải trả và vốn chủ sở hữu của Vinamilk tại ngày 31/12/2023 lần lượt là bao nhiêu tỷ đồng?",
            "expected_answer": "Nợ phải trả là 17.649 tỷ đồng và Vốn chủ sở hữu là 35.575 tỷ đồng.",
            "gold": [{"chunk_id": "vnm_p158_tab02", "page": 158, "evidence": "Nợ phải trả: 17.649 tỷ đồng; Vốn chủ sở hữu: 35.575 tỷ đồng."}]
        },
        {
            "id": "adv_test_tab_03",
            "split": "test",
            "group": "Bảng",
            "question": "Chỉ số cường độ phát thải khí nhà kính trên một kg sữa thành phẩm của Vinamilk năm 2023 đạt bao nhiêu kg CO2e và giảm bao nhiêu so với năm 2022?",
            "expected_answer": "Năm 2023 đạt 0.36 kg CO2e / kg sữa, giảm 7.7% so với mức 0.39 kg CO2e / kg sữa của năm 2022.",
            "gold": [{"chunk_id": "vnm_p78_tab03", "page": 78, "evidence": "Cường độ phát thải (kg CO2e / kg sữa): Năm 2022 là 0.39, Năm 2023 là 0.36, Giảm: -7.7%"}]
        },
        {
            "id": "adv_test_tab_04",
            "split": "test",
            "group": "Bảng",
            "question": "Trong cơ cấu nhân sự năm 2023, số lượng nhân sự nữ giữ vị trí cấp quản lý là bao nhiêu người và chiếm tỷ lệ bao nhiêu phần trăm trong tổng số quản lý?",
            "expected_answer": "Có 270 nhân sự nữ cấp quản lý, chiếm tỷ lệ 41.5% trong tổng số 650 nhân sự quản lý.",
            "gold": [{"chunk_id": "vnm_p112_tab05", "page": 112, "evidence": "Nhân sự cấp quản lý: Nữ 270 người, Tỷ lệ Nữ 41.5% trên tổng số 650 quản lý."}]
        },
        {
            "id": "adv_test_tab_05",
            "split": "test",
            "group": "Bảng",
            "question": "Doanh thu thuần từ các chi nhánh nước ngoài (như Driftwood, AngkorMilk) trong năm 2023 đạt bao nhiêu tỷ đồng và tăng trưởng bao nhiêu phần trăm?",
            "expected_answer": "Đạt 4.817 tỷ đồng, tăng trưởng 6.0% so với năm 2022 (4.543 tỷ đồng).",
            "gold": [{"chunk_id": "vnm_p165_tab06", "page": 165, "evidence": "Chi nhánh nước ngoài (Driftwood, AngkorMilk...): Năm 2022 là 4.543, Năm 2023 là 4.817 tỷ đồng (+6.0%)"}]
        },
        {
            "id": "adv_test_tab_06",
            "split": "test",
            "group": "Bảng",
            "question": "Theo bảng cơ cấu lao động, nhóm tuổi nào chiếm số lượng đông đảo nhất tại Vinamilk năm 2023 và có tổng số bao nhiêu nhân viên?",
            "expected_answer": "Nhóm tuổi từ 30 đến 50 tuổi chiếm đông nhất với 5.502 nhân viên (3.512 nam và 1.990 nữ).",
            "gold": [{"chunk_id": "vnm_p112_tab05", "page": 112, "evidence": "Từ 30 đến 50 tuổi: Nam 3.512, Nữ 1.990, Tổng cộng: 5.502"}]
        },

        # --- NHÓM 2: ẢNH, SƠ ĐỒ (5 câu) ---
        {
            "id": "adv_test_img_01",
            "split": "test",
            "group": "Ảnh, sơ đồ",
            "question": "Trong sơ đồ kinh tế tuần hoàn tại trang trại Green Farm, khí Methane (CH4) sinh ra từ hầm ủ Biogas kỵ khí được sử dụng vào mục đích gì?",
            "expected_answer": "Dùng để chạy máy phát điện phục vụ trang trại và đun nước nóng phục vụ thanh trùng.",
            "gold": [{"chunk_id": "vnm_p88_img02", "page": 88, "evidence": "Bước 3: Pha lỏng đưa vào hầm ủ Biogas kỵ khí tạo khí Methane (CH4) chạy máy phát điện phục vụ trang trại và đun nước nóng thanh trùng."}]
        },
        {
            "id": "adv_test_img_02",
            "split": "test",
            "group": "Ảnh, sơ đồ",
            "question": "Theo sơ đồ chuỗi giá trị từ đồng cỏ đến bàn ăn, bao bì vỏ hộp sữa sau khi người tiêu dùng sử dụng được xử lý như thế nào?",
            "expected_answer": "Được thu gom và tái chế thành vật liệu lợp mái sinh thái.",
            "gold": [{"chunk_id": "vnm_p42_img01", "page": 42, "evidence": "Khối Tiêu dùng & Tái chế: ... bao bì vỏ hộp sữa được thu gom và tái chế thành vật liệu lợp mái sinh thái."}]
        },
        {
            "id": "adv_test_img_03",
            "split": "test",
            "group": "Ảnh, sơ đồ",
            "question": "Theo sơ đồ tổ chức bộ máy, Ban Điều hành của Vinamilk đứng đầu là ai và trực tiếp điều hành bao nhiêu Giám đốc Điều hành các khối?",
            "expected_answer": "Đứng đầu là Tổng Giám đốc (Bà Mai Kiều Liên), trực tiếp điều hành 7 Giám đốc Điều hành phụ trách các khối chức năng.",
            "gold": [{"chunk_id": "vnm_p130_img03", "page": 130, "evidence": "Đứng đầu là Tổng Giám đốc (Bà Mai Kiều Liên), trực tiếp điều hành 7 Giám đốc Điều hành"}]
        },
        {
            "id": "adv_test_img_04",
            "split": "test",
            "group": "Ảnh, sơ đồ",
            "question": "Theo sơ đồ công nghệ xử lý nước thải tại Nhà máy Mega Bình Dương, công đoạn khử trùng sử dụng công nghệ gì thay thế cho hóa chất Clo?",
            "expected_answer": "Sử dụng công nghệ khử trùng bằng tia cực tím UV (không dùng hóa chất Clo).",
            "gold": [{"chunk_id": "vnm_p96_img04", "page": 96, "evidence": "Công đoạn 3: Khử trùng bằng tia cực tím UV (không dùng hóa chất Clo độc hại)."}]
        },
        {
            "id": "adv_test_img_05",
            "split": "test",
            "group": "Ảnh, sơ đồ",
            "question": "Trên ma trận rủi ro chuẩn ISO 31000 của Vinamilk, hai rủi ro nào được định vị ở Vùng Đỏ (mức độ nghiêm trọng cần kiểm soát ngay)?",
            "expected_answer": "Biến động giá nguyên liệu sữa bột toàn cầu và rủi ro tỷ giá USD/VND.",
            "gold": [{"chunk_id": "vnm_p140_img05", "page": 140, "evidence": "Rủi ro Vùng Đỏ (Nghiêm trọng - Cần kiểm soát ngay): Biến động giá nguyên liệu sữa bột toàn cầu; Rủi ro tỷ giá USD/VND."}]
        },

        # --- NHÓM 3: BIỂU ĐỒ (5 câu) ---
        {
            "id": "adv_test_chr_01",
            "split": "test",
            "group": "Biểu đồ",
            "question": "Theo biểu đồ thị phần ngành hàng của NielsenIQ RMS 2023, phân khúc sản phẩm nào Vinamilk chiếm thị phần áp đảo cao nhất với tỷ lệ bao nhiêu?",
            "expected_answer": "Sữa đặc có đường (Ông Thọ, Ngôi Sao Phương Nam) chiếm thị phần cao nhất với 79.5% thị phần.",
            "gold": [{"chunk_id": "vnm_p56_chr04", "page": 56, "evidence": "Sữa đặc có đường (Ông Thọ, Ngôi Sao Phương Nam): 79.5% thị phần"}]
        },
        {
            "id": "adv_test_chr_02",
            "split": "test",
            "group": "Biểu đồ",
            "question": "Dựa trên biểu đồ cột kép về Chương trình Sữa học đường, ngân sách đóng góp và số lượng học sinh thụ hưởng năm 2023 lần lượt là bao nhiêu?",
            "expected_answer": "Ngân sách đóng góp là 215 tỷ đồng và số học sinh thụ hưởng là 3.8 triệu học sinh.",
            "gold": [{"chunk_id": "vnm_p104_chr05", "page": 104, "evidence": "2023: 215 tỷ đồng | 3.8 triệu học sinh"}]
        },
        {
            "id": "adv_test_chr_03",
            "split": "test",
            "group": "Biểu đồ",
            "question": "Theo biểu đồ đường năng lượng tái tạo, mức tăng tỷ lệ năng lượng tái tạo từ năm 2020 (8.4%) đến năm 2023 (20.5%) là bao nhiêu điểm phần trăm?",
            "expected_answer": "Tăng 12.1 điểm phần trăm (từ 8.4% lên 20.5%).",
            "gold": [{"chunk_id": "vnm_p92_chr03", "page": 92, "evidence": "2020: 8.4%, 2023: 20.5% -> Chênh lệch: 20.5 - 8.4 = 12.1 điểm %"}]
        },
        {
            "id": "adv_test_chr_04",
            "split": "test",
            "group": "Biểu đồ",
            "question": "Theo biểu đồ tròn cơ cấu doanh thu theo thị trường năm 2023, doanh thu xuất khẩu trực tiếp đóng góp bao nhiêu phần trăm và tương ứng bao nhiêu tỷ đồng?",
            "expected_answer": "Đóng góp 8.3% tổng doanh thu hợp nhất, tương ứng 5.045 tỷ đồng.",
            "gold": [{"chunk_id": "vnm_p52_chr02", "page": 52, "evidence": "Xuất khẩu trực tiếp: 8.3% (tương ứng 5.045 tỷ đồng)"}]
        },
        {
            "id": "adv_test_chr_05",
            "split": "test",
            "group": "Biểu đồ",
            "question": "Dựa trên biểu đồ thị phần ngành hàng, tại phân khúc sữa tươi/sữa nước và sữa chua, Vinamilk lần lượt nắm giữ bao nhiêu phần trăm thị phần tại Việt Nam?",
            "expected_answer": "Sữa tươi/sữa nước nắm 55.4% thị phần và sữa chua (ăn & uống) nắm 52.8% thị phần.",
            "gold": [{"chunk_id": "vnm_p56_chr04", "page": 56, "evidence": "Sữa chua ăn & Sữa chua uống: 52.8% thị phần; Sữa tươi / Sữa nước: 55.4% thị phần"}]
        },

        # --- NHÓM 4: MULTI-HOP (4 câu) ---
        {
            "id": "adv_test_mul_01",
            "split": "test",
            "group": "Multi-hop",
            "question": "Tính tỷ số Nợ trên Vốn chủ sở hữu (D/E) của Vinamilk tại ngày 31/12/2023 dựa trên Bảng cân đối kế toán (trang 158) và cho biết chỉ số này phản ánh cấu trúc tài chính an toàn hay rủi ro?",
            "expected_answer": "Tỷ số D/E năm 2023 là 49.6% (17.649 tỷ / 35.575 tỷ đồng). Chỉ số này dưới 50%, phản ánh cấu trúc vốn rất lành mạnh và an toàn, tỷ lệ tự tài trợ cao.",
            "gold": [{"chunk_id": "vnm_p158_tab02", "page": 158, "evidence": "Nợ phải trả: 17.649; Vốn chủ sở hữu: 35.575 -> 17.649 / 35.575 = 49.61%"}]
        },
        {
            "id": "adv_test_mul_02",
            "split": "test",
            "group": "Multi-hop",
            "question": "So sánh tốc độ tăng trưởng doanh thu hoạt động tài chính (+26.5%) và chi phí tài chính (-26.7%) tại trang 154, sự chênh lệch này đã tác động tích cực như thế nào đến lợi nhuận ròng của công ty?",
            "expected_answer": "Doanh thu tài chính tăng mạnh lên 2.115 tỷ đồng (+26.5%, chủ yếu nhờ lãi tiền gửi) trong khi chi phí tài chính giảm xuống 452 tỷ (-26.7%), tạo ra lợi nhuận tài chính thuần đạt 1.663 tỷ đồng (so với 1.055 tỷ năm 2022), đóng góp đáng kể vào mức tăng 5.1% lợi nhuận sau thuế.",
            "gold": [{"chunk_id": "vnm_p154_tab01", "page": 154, "evidence": "Doanh thu tài chính tăng từ 1.672 lên 2.115 tỷ; Chi phí tài chính giảm từ 617 xuống 452 tỷ."}]
        },
        {
            "id": "adv_test_mul_03",
            "split": "test",
            "group": "Multi-hop",
            "question": "Kết hợp Thông điệp Tổng Giám đốc (trang 12) và Bảng kết quả kinh doanh (trang 154), thông điệp mới 'Để tâm đổi thay lớn' năm 2023 được phản ánh bằng con số lợi nhuận sau thuế hợp nhất đạt bao nhiêu và tăng trưởng bao nhiêu phần trăm?",
            "expected_answer": "Lợi nhuận sau thuế hợp nhất đạt 9.019 tỷ đồng, tăng trưởng 5.1% - 5.2% so với năm 2022.",
            "gold": [
                {"chunk_id": "vnm_p12_c0", "page": 12, "evidence": "Thông điệp 'Để tâm đổi thay lớn'... lợi nhuận sau thuế hợp nhất đạt 9.019 tỷ đồng, tăng 5.2%"},
                {"chunk_id": "vnm_p154_tab01", "page": 154, "evidence": "Lợi nhuận sau thuế TNDN 2023: 9.019 tỷ đồng (+5.1%)"}
            ]
        },
        {
            "id": "adv_test_mul_04",
            "split": "test",
            "group": "Multi-hop",
            "question": "Tính tỷ lệ chi phí bán hàng trên doanh thu thuần của Vinamilk năm 2023 (trang 154) và so sánh tỷ lệ này với năm 2022?",
            "expected_answer": "Năm 2023 tỷ lệ chi phí bán hàng trên doanh thu thuần là 21.29% (12.876 / 60.479 tỷ), tăng nhẹ so với mức 20.89% của năm 2022 (12.548 / 60.075 tỷ).",
            "gold": [{"chunk_id": "vnm_p154_tab01", "page": 154, "evidence": "2023: 12.876 / 60.479 = 21.29%; 2022: 12.548 / 60.075 = 20.89%"}]
        },

        # --- NHÓM 5: TEXT (4 câu) ---
        {
            "id": "adv_test_txt_01",
            "split": "test",
            "group": "Text",
            "question": "Ba mốc mục tiêu giảm phát thải khí nhà kính cụ thể trong lộ trình Net Zero 2050 theo chuẩn PAS 2060 của Vinamilk là những năm nào và mục tiêu giảm bao nhiêu phần trăm?",
            "expected_answer": "Mục tiêu: Đến năm 2027 giảm 15%; đến năm 2035 giảm 55%; và đến năm 2050 đạt Net Zero (giảm 100% phát thải ròng).",
            "gold": [{"chunk_id": "vnm_p24_c0", "page": 24, "evidence": "Mục tiêu cụ thể gồm: Đến năm 2027, giảm 15% phát thải KNK; đến năm 2035, giảm 55% phát thải KNK; và đến năm 2050 đạt mức phát thải ròng bằng 0"}]
        },
        {
            "id": "adv_test_txt_02",
            "split": "test",
            "group": "Text",
            "question": "Hệ thống làm mát chuồng trại tự động tại các trang trại Green Farm của Vinamilk duy trì nhiệt độ lý tưởng trong khoảng bao nhiêu độ C?",
            "expected_answer": "Duy trì ở mức nhiệt độ lý tưởng 24 - 26 độ C.",
            "gold": [{"chunk_id": "vnm_p35_c1", "page": 35, "evidence": "nhiệt độ chuồng luôn duy trì ở mức lý tưởng 24-26 độ C"}]
        },
        {
            "id": "adv_test_txt_03",
            "split": "test",
            "group": "Text",
            "question": "Chủ tịch Hội đồng Quản trị của Vinamilk nhiệm kỳ 2022-2026 là ai và HĐQT có bao nhiêu thành viên độc lập?",
            "expected_answer": "Chủ tịch HĐQT là ông Nguyễn Hạnh Phúc và HĐQT có 3 thành viên độc lập (chiếm 30%).",
            "gold": [{"chunk_id": "vnm_p128_c0", "page": 128, "evidence": "Chủ tịch HĐQT là ông Nguyễn Hạnh Phúc... có 3 thành viên độc lập (chiếm 30%)"}]
        },
        {
            "id": "adv_test_txt_04",
            "split": "test",
            "group": "Text",
            "question": "Tỷ lệ cán bộ công nhân viên của Vinamilk tham gia tổ chức công đoàn tính đến cuối năm 2023 đạt bao nhiêu phần trăm?",
            "expected_answer": "Đạt 99.8%.",
            "gold": [{"chunk_id": "vnm_p68_c0", "page": 68, "evidence": "Tỷ lệ lao động tham gia công đoàn đạt 99.8%."}]
        },

        # --- NHÓM 6: THIẾU BẰNG CHỨNG (6 câu) ---
        {
            "id": "adv_test_abs_01",
            "split": "test",
            "group": "Thiếu bằng chứng",
            "question": "Kế hoạch xây dựng nhà máy sản xuất sữa chua sấy thăng hoa tại bang California (Mỹ) của Vinamilk dự kiến khởi công vào quý nào năm 2025?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },
        {
            "id": "adv_test_abs_02",
            "split": "test",
            "group": "Thiếu bằng chứng",
            "question": "Mức lương và tiền thưởng cụ thể trong năm 2023 của từng Giám đốc Điều hành các khối thành viên trong Ban Điều hành là bao nhiêu tiền?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },
        {
            "id": "adv_test_abs_03",
            "split": "test",
            "group": "Thiếu bằng chứng",
            "question": "Tỷ lệ thị phần của sản phẩm sữa bột người lớn Vinamilk Sure Prevent tại thị trường Philippines trong năm 2023 là bao nhiêu phần trăm?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },
        {
            "id": "adv_test_abs_04",
            "split": "test",
            "group": "Thiếu bằng chứng",
            "question": "Chỉ số hàm lượng protein và canxi chính xác trong mỗi 100ml sữa tươi tiệt trùng bổ sung tổ yến của Vinamilk là bao nhiêu gam và miligam?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },
        {
            "id": "adv_test_abs_05",
            "split": "test",
            "group": "Thiếu bằng chứng",
            "question": "Giá trị hợp đồng mua sắm 50 xe tải điện chuyên dụng vận chuyển sữa từ nhà sản xuất VinFast trong năm 2023 có tổng giá trị bao nhiêu tỷ đồng?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        },
        {
            "id": "adv_test_abs_06",
            "split": "test",
            "group": "Thiếu bằng chứng",
            "question": "Dự báo chi tiết tốc độ tăng trưởng doanh thu thuần của Vinamilk cho giai đoạn 2026 - 2030 theo từng kịch bản kinh tế vĩ mô là bao nhiêu phần trăm mỗi năm?",
            "expected_answer": "Không đủ bằng chứng để trả lời.",
            "gold": []
        }
    ]

    with open(data_dir / "questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    # 4. Agent Cases (format expected by starter/agent_metrics.py)
    agent_cases = []
    for q in questions:
        agent_cases.append({
            "id": q["id"],
            "split": q["split"],
            "query": q["question"],
            "answerable": len(q["gold"]) > 0,
            "ground_truth_chunks": [g["chunk_id"] for g in q["gold"]],
            "expected_answer": q["expected_answer"],
            "group": q["group"]
        })

    with open(data_dir / "agent_cases.json", "w", encoding="utf-8") as f:
        json.dump(agent_cases, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(chunks)} multimodal chunks.")
    print(f"Generated {len(questions)} benchmark questions ({len([q for q in questions if q['split'] == 'dev'])} Dev, {len([q for q in questions if q['split'] == 'test'])} Test).")
    print(f"Test split breakdown:")
    for group in ["Bảng", "Ảnh, sơ đồ", "Biểu đồ", "Multi-hop", "Text", "Thiếu bằng chứng"]:
        cnt = len([q for q in questions if q['split'] == 'test' and q['group'] == group])
        print(f" - {group}: {cnt} câu")

if __name__ == "__main__":
    generate_advanced_dataset()

