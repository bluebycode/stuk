class AddPkToUser < ActiveRecord::Migration[5.2]
  def change
    add_column :users, :public_key, :text
  end
end
