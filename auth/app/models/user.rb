class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable

  before_create :complete_registration

  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable

  devise :two_factor_authenticatable,
         :otp_secret_encryption_key => "hsfdbbhsjhdbndn&&6GFF87654678r90hbvgfcxvGF"

  def activate_otp
    self.otp_required_for_login = true
    self.otp_secret = unconfirmed_otp_secret
    self.unconfirmed_otp_secret = nil
    save!
  end

  def deactivate_otp
    self.otp_required_for_login = false
    self.otp_secret = nil
    save!
  end

  def complete_registration
    self.role = 'Estudiante'
    self.salt = SecureRandom.hex
  end
end
