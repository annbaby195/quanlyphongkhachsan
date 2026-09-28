import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ============================================================
# CẤU HÌNH ỨNG DỤNG
# ============================================================

st.set_page_config(
    page_title="Hotel Manager",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS GIAO DIỆN
# ============================================================

st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #6b7280;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .room-card {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
    }

    .status-green {
        color: #16a34a;
        font-weight: 700;
    }

    .status-blue {
        color: #2563eb;
        font-weight: 700;
    }

    .status-yellow {
        color: #ca8a04;
        font-weight: 700;
    }

    .status-red {
        color: #dc2626;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DỮ LIỆU MẶC ĐỊNH
# ============================================================

ROOM_DATA = [
    ["101", "Standard", 500000, "Trống"],
    ["102", "Standard", 500000, "Đang ở"],
    ["103", "Standard", 500000, "Trống"],
    ["104", "Deluxe", 700000, "Trống"],
    ["105", "Deluxe", 700000, "Đang dọn"],

    ["201", "Standard", 500000, "Trống"],
    ["202", "Standard", 500000, "Đang ở"],
    ["203", "Deluxe", 700000, "Trống"],
    ["204", "Deluxe", 700000, "Bảo trì"],
    ["205", "Suite", 1200000, "Trống"],

    ["301", "Standard", 500000, "Trống"],
    ["302", "Deluxe", 700000, "Đang ở"],
    ["303", "Deluxe", 700000, "Trống"],
    ["304", "Suite", 1200000, "Trống"],
    ["305", "Suite", 1200000, "Trống"],

    ["401", "Standard", 500000, "Trống"],
    ["402", "Deluxe", 700000, "Trống"],
    ["403", "Deluxe", 700000, "Trống"],
    ["404", "Suite", 1200000, "Trống"],
    ["405", "Suite", 1200000, "Bảo trì"],
]


# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = pd.DataFrame(
        ROOM_DATA,
        columns=["Phòng", "Loại phòng", "Giá/đêm", "Trạng thái"]
    )

if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame(
        columns=[
            "Mã đặt phòng",
            "Phòng",
            "Tên khách",
            "Số điện thoại",
            "Ngày nhận",
            "Ngày trả",
            "Số đêm",
            "Tiền phòng",
            "Dịch vụ",
            "Tổng tiền",
            "Trạng thái"
        ]
    )

if "services" not in st.session_state:
    st.session_state.services = pd.DataFrame([
        ["DV001", "Nước suối", 20000],
        ["DV002", "Cà phê", 40000],
        ["DV003", "Ăn sáng", 100000],
        ["DV004", "Giặt ủi", 80000],
        ["DV005", "Minibar", 50000],
        ["DV006", "Extra Bed", 200000],
    ], columns=["Mã DV", "Tên dịch vụ", "Đơn giá"])


# ============================================================
# HÀM HỖ TRỢ
# ============================================================

def money(value):
    return f"{int(value):,} VNĐ"


def get_room_status_count(status):
    return len(
        st.session_state.rooms[
            st.session_state.rooms["Trạng thái"] == status
        ]
    )


def update_room_status(room_number, status):
    index = st.session_state.rooms.index[
        st.session_state.rooms["Phòng"] == room_number
    ]

    if len(index) > 0:
        st.session_state.rooms.loc[
            index[0], "Trạng thái"
        ] = status


def create_booking_id():
    return f"BK{len(st.session_state.bookings) + 1:04d}"


def active_bookings():
    return st.session_state.bookings[
        st.session_state.bookings["Trạng thái"] == "Đang ở"
    ]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# 🏨 Hotel Manager")
st.sidebar.caption("Hệ thống quản lý khách sạn")

st.sidebar.divider()

menu = st.sidebar.radio(
    "MENU",
    [
        "📊 Tổng quan",
        "🛏️ Quản lý phòng",
        "🛎️ Check-in",
        "🚪 Check-out",
        "👥 Khách lưu trú",
        "🍽️ Dịch vụ",
        "💰 Doanh thu",
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Hệ thống demo quản lý phòng khách sạn\n\n"
    "Quản lý trạng thái phòng, khách lưu trú, "
    "check-in, check-out, dịch vụ và doanh thu."
)


# ============================================================
# 1. DASHBOARD
# ============================================================

if menu == "📊 Tổng quan":

    st.markdown(
        '<div class="main-title">📊 Tổng quan khách sạn</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Theo dõi tình trạng phòng và hoạt động lưu trú'
        '</div>',
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms

    total_rooms = len(rooms)
    empty_rooms = get_room_status_count("Trống")
    occupied_rooms = get_room_status_count("Đang ở")
    cleaning_rooms = get_room_status_count("Đang dọn")
    maintenance_rooms = get_room_status_count("Bảo trì")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("🏨 Tổng phòng", total_rooms)
    col2.metric("🟢 Phòng trống", empty_rooms)
    col3.metric("🔵 Đang ở", occupied_rooms)
    col4.metric("🟡 Đang dọn", cleaning_rooms)
    col5.metric("🔴 Bảo trì", maintenance_rooms)

    st.divider()

    # Tỷ lệ lấp đầy
    occupancy = (
        occupied_rooms / total_rooms * 100
        if total_rooms > 0 else 0
    )

    st.subheader("📈 Công suất phòng")

    st.progress(
        int(occupancy),
        text=f"Công suất hiện tại: {occupancy:.1f}%"
    )

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:

        st.subheader("🛏️ Trạng thái phòng")

        status_data = pd.DataFrame({
            "Trạng thái": [
                "Trống",
                "Đang ở",
                "Đang dọn",
                "Bảo trì"
            ],
            "Số phòng": [
                empty_rooms,
                occupied_rooms,
                cleaning_rooms,
                maintenance_rooms
            ]
        })

        st.dataframe(
            status_data,
            use_container_width=True,
            hide_index=True
        )

    with col_right:

        st.subheader("👥 Khách đang lưu trú")

        current = active_bookings()

        if current.empty:
            st.info("Chưa có khách đang lưu trú.")
        else:
            st.dataframe(
                current[
                    [
                        "Phòng",
                        "Tên khách",
                        "Ngày nhận",
                        "Ngày trả"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    st.subheader("📋 Danh sách phòng")

    display = rooms.copy()

    display["Giá/đêm"] = display["Giá/đêm"].apply(money)

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 2. QUẢN LÝ PHÒNG
# ============================================================

elif menu == "🛏️ Quản lý phòng":

    st.markdown(
        '<div class="main-title">🛏️ Quản lý phòng</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Cập nhật tình trạng phòng và theo dõi danh sách phòng."
    )

    rooms = st.session_state.rooms

    col1, col2 = st.columns(2)

    with col1:

        selected_room = st.selectbox(
            "Chọn phòng",
            rooms["Phòng"].tolist()
        )

    current_status = rooms.loc[
        rooms["Phòng"] == selected_room,
        "Trạng thái"
    ].iloc[0]

    with col2:

        statuses = [
            "Trống",
            "Đang ở",
            "Đang dọn",
            "Bảo trì"
        ]

        new_status = st.selectbox(
            "Trạng thái mới",
            statuses,
            index=statuses.index(current_status)
        )

    if st.button(
        "💾 Cập nhật trạng thái",
        use_container_width=True
    ):

        update_room_status(
            selected_room,
            new_status
        )

        st.success(
            f"Phòng {selected_room} đã được cập nhật thành "
            f"'{new_status}'."
        )

        st.rerun()

    st.divider()

    st.subheader("🔎 Bộ lọc phòng")

    filter_status = st.selectbox(
        "Lọc theo trạng thái",
        ["Tất cả"] + statuses
    )

    filtered_rooms = rooms.copy()

    if filter_status != "Tất cả":
        filtered_rooms = filtered_rooms[
            filtered_rooms["Trạng thái"] == filter_status
        ]

    filtered_rooms["Giá/đêm"] = filtered_rooms[
        "Giá/đêm"
    ].apply(money)

    st.dataframe(
        filtered_rooms,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 3. CHECK-IN
# ============================================================

elif menu == "🛎️ Check-in":

    st.markdown(
        '<div class="main-title">🛎️ Check-in khách</div>',
        unsafe_allow_html=True
    )

    available = st.session_state.rooms[
        st.session_state.rooms["Trạng thái"] == "Trống"
    ]

    if available.empty:

        st.warning(
            "Hiện tại không còn phòng trống."
        )

    else:

        with st.form("checkin_form"):

            col1, col2 = st.columns(2)

            with col1:

                room = st.selectbox(
                    "🛏️ Phòng",
                    available["Phòng"].tolist()
                )

                guest_name = st.text_input(
                    "👤 Họ và tên khách"
                )

                phone = st.text_input(
                    "📱 Số điện thoại"
                )

            with col2:

                checkin_date = st.date_input(
                    "📅 Ngày nhận phòng",
                    value=date.today()
                )

                checkout_date = st.date_input(
                    "📅 Ngày trả phòng",
                    value=date.today() + timedelta(days=1)
                )

                service_fee = st.number_input(
                    "🍽️ Dịch vụ ban đầu",
                    min_value=0,
                    value=0,
                    step=50000
                )

            submit = st.form_submit_button(
                "🛎️ XÁC NHẬN CHECK-IN",
                use_container_width=True
            )

        if submit:

            if not guest_name.strip():

                st.error(
                    "Vui lòng nhập tên khách."
                )

            elif not phone.strip():

                st.error(
                    "Vui lòng nhập số điện thoại."
                )

            elif checkout_date <= checkin_date:

                st.error(
                    "Ngày trả phòng phải sau ngày nhận phòng."
                )

            else:

                nights = (
                    checkout_date - checkin_date
                ).days

                room_price = int(
                    st.session_state.rooms.loc[
                        st.session_state.rooms["Phòng"] == room,
                        "Giá/đêm"
                    ].iloc[0]
                )

                room_total = nights * room_price

                total = room_total + service_fee

                booking = pd.DataFrame([{
                    "Mã đặt phòng": create_booking_id(),
                    "Phòng": room,
                    "Tên khách": guest_name.strip(),
                    "Số điện thoại": phone.strip(),
                    "Ngày nhận": checkin_date,
                    "Ngày trả": checkout_date,
                    "Số đêm": nights,
                    "Tiền phòng": room_total,
                    "Dịch vụ": service_fee,
                    "Tổng tiền": total,
                    "Trạng thái": "Đang ở"
                }])

                st.session_state.bookings = pd.concat(
                    [
                        st.session_state.bookings,
                        booking
                    ],
                    ignore_index=True
                )

                update_room_status(
                    room,
                    "Đang ở"
                )

                st.success(
                    f"Check-in thành công cho {guest_name}."
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Phòng",
                    room
                )

                col2.metric(
                    "Số đêm",
                    nights
                )

                col3.metric(
                    "Tạm tính",
                    money(total)
                )


# ============================================================
# 4. CHECK-OUT
# ============================================================

elif menu == "🚪 Check-out":

    st.markdown(
        '<div class="main-title">🚪 Check-out</div>',
        unsafe_allow_html=True
    )

    current = active_bookings()

    if current.empty:

        st.info(
            "Hiện không có khách nào đang lưu trú."
        )

    else:

        room = st.selectbox(
            "Chọn phòng check-out",
            current["Phòng"].tolist()
        )

        booking_index = current.index[
            current["Phòng"] == room
        ][0]

        booking = st.session_state.bookings.loc[
            booking_index
        ]

        st.subheader("👤 Thông tin khách")

        col1, col2, col3 = st.columns(3)

        col1.write(
            f"**Khách:** {booking['Tên khách']}"
        )

        col2.write(
            f"**Điện thoại:** {booking['Số điện thoại']}"
        )

        col3.write(
            f"**Số đêm:** {booking['Số đêm']}"
        )

        st.divider()

        room_money = int(booking["Tiền phòng"])
        old_service = int(booking["Dịch vụ"])

        extra_service = st.number_input(
            "🍽️ Dịch vụ phát sinh",
            min_value=0,
            value=old_service,
            step=50000
        )

        total = room_money + extra_service

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"Tiền phòng: **{money(room_money)}**"
            )

            st.write(
                f"Tiền dịch vụ: **{money(extra_service)}**"
            )

        with col2:

            st.metric(
                "💰 TỔNG THANH TOÁN",
                money(total)
            )

        if st.button(
            "💳 THANH TOÁN & CHECK-OUT",
            use_container_width=True
        ):

            st.session_state.bookings.loc[
                booking_index,
                "Dịch vụ"
            ] = extra_service

            st.session_state.bookings.loc[
                booking_index,
                "Tổng tiền"
            ] = total

            st.session_state.bookings.loc[
                booking_index,
                "Trạng thái"
            ] = "Đã trả phòng"

            update_room_status(
                room,
                "Đang dọn"
            )

            st.success(
                f"Đã hoàn tất check-out phòng {room}."
            )

            st.info(
                "Phòng đã chuyển sang trạng thái 'Đang dọn'."
            )

            st.rerun()


# ============================================================
# 5. KHÁCH ĐANG LƯU TRÚ
# ============================================================

elif menu == "👥 Khách lưu trú":

    st.markdown(
        '<div class="main-title">👥 Khách đang lưu trú</div>',
        unsafe_allow_html=True
    )

    current = active_bookings()

    if current.empty:

        st.info(
            "Hiện không có khách đang lưu trú."
        )

    else:

        display = current.copy()

        display["Tiền phòng"] = display[
            "Tiền phòng"
        ].apply(money)

        display["Dịch vụ"] = display[
            "Dịch vụ"
        ].apply(money)

        display["Tổng tiền"] = display[
            "Tổng tiền"
        ].apply(money)

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("🔎 Chi tiết khách")

        selected = st.selectbox(
            "Chọn khách",
            current["Tên khách"].tolist()
        )

        detail = current[
            current["Tên khách"] == selected
        ].iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.write(
            f"**Phòng:** {detail['Phòng']}"
        )

        col2.write(
            f"**Ngày nhận:** {detail['Ngày nhận']}"
        )

        col3.write(
            f"**Ngày trả:** {detail['Ngày trả']}"
        )


# ============================================================
# 6. DỊCH VỤ
# ============================================================

elif menu == "🍽️ Dịch vụ":

    st.markdown(
        '<div class="main-title">🍽️ Quản lý dịch vụ</div>',
        unsafe_allow_html=True
    )

    services = st.session_state.services.copy()

    services["Đơn giá"] = services[
        "Đơn giá"
    ].apply(money)

    st.dataframe(
        services,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("➕ Thêm dịch vụ")

    with st.form("service_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            service_name = st.text_input(
                "Tên dịch vụ"
            )

        with col2:
            service_price = st.number_input(
                "Đơn giá",
                min_value=0,
                value=0,
                step=10000
            )

        with col3:
            service_code = st.text_input(
                "Mã dịch vụ"
            )

        add_service = st.form_submit_button(
            "➕ Thêm dịch vụ",
            use_container_width=True
        )

    if add_service:

        if not service_name.strip():

            st.error(
                "Vui lòng nhập tên dịch vụ."
            )

        elif not service_code.strip():

            st.error(
                "Vui lòng nhập mã dịch vụ."
            )

        else:

            new_service = pd.DataFrame([{
                "Mã DV": service_code.upper(),
                "Tên dịch vụ": service_name,
                "Đơn giá": service_price
            }])

            st.session_state.services = pd.concat(
                [
                    st.session_state.services,
                    new_service
                ],
                ignore_index=True
            )

            st.success(
                "Đã thêm dịch vụ."
            )

            st.rerun()


# ============================================================
# 7. DOANH THU
# ============================================================

elif menu == "💰 Doanh thu":

    st.markdown(
        '<div class="main-title">💰 Doanh thu</div>',
        unsafe_allow_html=True
    )

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có dữ liệu doanh thu."
        )

    else:

        paid = bookings[
            bookings["Trạng thái"] == "Đã trả phòng"
        ]

        total_revenue = paid["Tổng tiền"].sum()
        room_revenue = paid["Tiền phòng"].sum()
        service_revenue = paid["Dịch vụ"].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Tổng doanh thu",
            money(total_revenue)
        )

        col2.metric(
            "🛏️ Doanh thu phòng",
            money(room_revenue)
        )

        col3.metric(
            "🍽️ Doanh thu dịch vụ",
            money(service_revenue)
        )

        st.divider()

        st.subheader("📋 Lịch sử giao dịch")

        history = paid.copy()

        history["Tiền phòng"] = history[
            "Tiền phòng"
        ].apply(money)

        history["Dịch vụ"] = history[
            "Dịch vụ"
        ].apply(money)

        history["Tổng tiền"] = history[
            "Tổng tiền"
        ].apply(money)

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("📊 Thống kê theo loại phòng")

        if not paid.empty:

            revenue_by_room = paid.groupby(
                "Phòng"
            )["Tổng tiền"].sum().reset_index()

            revenue_by_room["Tổng tiền"] = (
                revenue_by_room["Tổng tiền"]
                .apply(money)
            )

            st.dataframe(
                revenue_by_room,
                use_container_width=True,
                hide_index=True
            )
