class User < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable

  before_create :complete_registration

  def complete_registration
    self.role = 'Estudiante'
    self.salt = SecureRandom.hex
  end
end
