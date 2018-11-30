require 'json'

class Machine < ApplicationRecord

  before_create :ensure_image

  def ensure_image
    self.image_src = 'https://www2.fgcu.edu/BTS/images/optiplex5040.jpg' if image_src.blank?
  end

  def generate_config_json(email)
    { name: name,
      ip: ip,
      sequence: sequence,
      email: email }.to_json
  end
end
