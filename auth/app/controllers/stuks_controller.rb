require 'barby'
require 'barby/barcode'
require 'barby/barcode/qr_code'
require 'barby/outputter/png_outputter'

class StuksController < ApplicationController
  before_action :authenticate_user!, except: [:verify, :verify_test]

  def index; end

  def verify_test
    respond_to do |format|
      format.json { render json: { verify: true,
                                   user: 'zel@stuk.com ',
                                   domain: 'stuk.com',
                                   token: 2343455 } }
    end
  end

  def verify
    seq = params[:user_domain_token]
    decrypted_seq = Base64.decode64(seq)
    user_info = decrypted_seq.split("/")

    respond_to do |format|
      format.json { render json: { verify: true,
                                   user: user_info[0],
                                   domain: user_info[1],
                                   token: user_info[2] } }
    end
  end

  def install_gauth
    return :forbidden if current_user.otp_required_for_login
    current_user.unconfirmed_otp_secret = User.generate_otp_secret
    current_user.save!
    @qr_code = RQRCode::QRCode.new(two_factor_url).to_img.resize(280, 280).to_data_url
    current_user.activate_otp
  end

  def uninstall_gauth
    return :forbidden unless current_user.otp_required_for_login
    current_user.deactivate_otp
    redirect_back(fallback_location: root_path)
  end

  private

  def two_factor_url
    app_id = "zel"
    app_name = "stuk.com"
    "otpauth://totp/#{app_id}:#{current_user.email}?secret=#{current_user.unconfirmed_otp_secret}&issuer=#{app_name}"
  end
end
