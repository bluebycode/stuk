require 'barby'
require 'barby/barcode'
require 'barby/barcode/qr_code'
require 'barby/outputter/png_outputter'

class StuksController < ApplicationController

  def index
    @user = current_user
  end

  def verify_test
    respond_to do |format|
      format.json { render json: { verify: true } }
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
end
