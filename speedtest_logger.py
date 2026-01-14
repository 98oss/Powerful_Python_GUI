import speedtest
import time

def download():
    try:
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()
        time.sleep(1)
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        return f"Download speed: {download_speed:.2f} Mbps"
    except Exception as e:
        return f"Download error: {str(e)}"


def upload():
    try:
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()
        time.sleep(1)
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        return f"Upload speed: {upload_speed:.2f} Mbps"
    except Exception as e:
        return f"Upload error: {str(e)}"