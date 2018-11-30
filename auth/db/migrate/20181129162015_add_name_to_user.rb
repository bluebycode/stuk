class AddNameToUser < ActiveRecord::Migration[5.2]
  def change
    add_column :users, :name, :string
    add_column :users, :surname, :string
    add_column :users, :role, :string
    add_column :users, :grade, :string
    add_column :users, :salt, :string
  end
end
