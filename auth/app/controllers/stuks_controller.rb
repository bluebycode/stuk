require 'zip'
require 'barby'
require 'barby/barcode'
require 'barby/barcode/qr_code'
require 'barby/outputter/png_outputter'
require 'json'

class StuksController < ApplicationController
  before_action :authenticate_user!, except: %i[verify verify_test]

  def index
    redirect_to admin_dashboard_path if current_user.admin?
    @machines = Machine.where(id: current_user.user_machines.pluck(:machine_id))
  end

  def admin_dashboard
    redirect_to root_path unless current_user.admin?
    @machines = Machine.all
    @machine = Machine.new
  end

  def generate_config
    machine = Machine.find(params[:id])
    config_json = machine.generate_config_json(current_user.email)
    send_data config_json, filename: 'configs.json'
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
    ap(verify: correct_otp, user: user_info[0], domain: user_info[1], token: user_info[2])
    respond_to do |format|
      format.json do
        render json: { verify: correct_otp,
                       user: user_info[0],
                       domain: user_info[1],
                       token: user_info[2] }
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

  def two_factor_url
    app_id = 'zel'
    app_name = 'stuk.com'
    "otpauth://totp/#{app_id}:#{current_user.email}?secret=#{current_user.unconfirmed_otp_secret}&issuer=#{app_name}"
  end
end
