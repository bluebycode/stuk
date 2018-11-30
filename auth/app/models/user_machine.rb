class UserMachine < ApplicationRecord
  belongs_to :user
  belongs_to :machine

  validates :machine_username, presence: true

  before_create :generate_username

  def generate_username
    username = user.email.split('@')[0].gsub(/[^0-9A-Za-z]/, '') # name w/o special chars
    while machine_username.blank?
      if unique_username(id, username)
        self.machine_username = username
      else
        username += rand.to_s[2..5]
      end
    end
  end

  def unique_username(machine_id, username)
    ums = UserMachine.where(machine_id: machine_id, machine_username: username)
    ums.count.zero?
  end
end
