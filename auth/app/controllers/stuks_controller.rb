require 'zip'
require 'barby'
require 'barby/barcode'
require 'barby/barcode/qr_code'
require 'barby/outputter/png_outputter'

class StuksController < ApplicationController
  before_action :authenticate_user!, except: %i[verify verify_test]

  def index; end

  def admin_dashboard
    head :forbidden unless current_user.admin?
  end

  def generate_keys
    keys_zip = generate_ssh_kp_zip(current_user.email)
    send_data keys_zip, filename: 'claves_stuk.zip'
  end

  def verify_test
    respond_to do |format|
      format.json do
        render json: { verify: true,
                       user: 'zel@stuk.com ',
                       domain: 'stuk.com',
                       token: 243_455 }
      end
    end
  end

  def verify
    seq = params[:user_domain_token]
    decrypted_seq = Base64.decode64(seq)
    user_info = decrypted_seq.split(';') # 0: user, 1: domain, 2: OTP, 3: PubKey
    user = User.find_by(email: user_info[0])

    correct_otp = user.validate_and_consume_otp!(user_info[2], otp_secret: user.otp_secret)
    correct_public_key = user.public_key == user_info[3]
    validation = correct_otp && correct_public_key
    respond_to do |format|
      format.json do
        render json: { verify: validation,
                       user: user_info[0],
                       domain: user_info[1],
                       token: user_info[2],
                       public_key: user_info[3] }
      end
    end
  end

  # Fuente: https://alisafrunza.github.io/rails/two-factor-auth.html
  def install_gauth
    return :forbidden if current_user.otp_required_for_login

    current_user.unconfirmed_otp_secret = User.generate_otp_secret
    current_user.save!
    @qr_code = RQRCode::QRCode.new(two_factor_url).to_img.resize(280, 280).to_data_url
    current_user.activate_otp
  end

  # Fuente: https://alisafrunza.github.io/rails/two-factor-auth.html
  def uninstall_gauth
    return :forbidden unless current_user.otp_required_for_login

    current_user.deactivate_otp
    redirect_back(fallback_location: root_path)
  end

  private

  def generate_ssh_kp_zip(email)
    ssh_kp = SSHKey.generate(type: 'RSA',
                             bits: 1024,
                             comment: email)
    current_user.update!(public_key: ssh_kp.public_key)
    # Basado en https://stackoverflow.com/questions/2405921/how-can-i-generate-zip-file-without-saving-to-the-disk-with-ruby?rq=1
    stringio = ::Zip::OutputStream.write_buffer do |zio|
      zio.put_next_entry('id_rsa_stuk')
      zio.write(ssh_kp.private_key)
      zio.put_next_entry('id_rsa_stuk.pub')
      zio.write(ssh_kp.public_key)
    end
    stringio.string
  end

  def two_factor_url
    app_id = 'zel'
    app_name = 'stuk.com'
    "otpauth://totp/#{app_id}:#{current_user.email}?secret=#{current_user.unconfirmed_otp_secret}&issuer=#{app_name}"
  end
end
