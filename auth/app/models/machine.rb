require 'json'

class Machine < ApplicationRecord

  def generate_config_json(email)

    config_json = {
        name: self.name,
        ip: self.ip,
        sequence: self.sequence,
        email: email
    }.to_json
  end

end
