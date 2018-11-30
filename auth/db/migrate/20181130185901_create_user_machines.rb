class CreateUserMachines < ActiveRecord::Migration[5.2]
  def change
    create_table :user_machines do |t|
      t.belongs_to :user, foreign_key: true
      t.belongs_to :machine, foreign_key: true
      t.string :machine_username

      t.timestamps
    end
  end
end
