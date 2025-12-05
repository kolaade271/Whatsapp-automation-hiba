import pymysql
import sys

def setup_mysql():
    print("🔌 Connecting to MySQL (XAMPP default)...")
    
    # XAMPP default credentials
    host = "localhost"
    user = "root"
    password = ""  # Default is empty
    port = 3306
    
    try:
        # Connect to MySQL server
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        print("✅ Connected to MySQL server!")
        
        # Create database
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS wafr_bot")
        print("✅ Database 'wafr_bot' created/verified!")
        
        cursor.close()
        conn.close()
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"❌ TCP Connection failed: {e}")
        print("🔄 Trying XAMPP Socket connection...")
        
        try:
            # Try connecting via socket
            conn = pymysql.connect(
                user=user,
                password=password,
                unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
            )
            print("✅ Connected to MySQL via Socket!")
            
            # Create database
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS wafr_bot")
            print("✅ Database 'wafr_bot' created/verified!")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as socket_error:
            print(f"❌ Socket Connection failed: {socket_error}")
            print("\nPossible fixes:")
            print("1. Make sure XAMPP MySQL is running (Green light)")
            print("2. Check if you have a password set for root user")
            print("3. Verify XAMPP installation path")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = setup_mysql()
    if not success:
        sys.exit(1)
