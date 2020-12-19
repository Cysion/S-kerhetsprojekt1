
from sys import exit
from time import time

from django.test import TestCase
from login.tools import registerUser
from userprofile.tools import createRelation, updateRelationTo, showAllRelationsFrom


class TestStress(TestCase):
    """ Stress-test for user relations """

    n_professionals = 5
    users_per_professional = 3
    n_norm_users = n_professionals * users_per_professional

    permissions = "11111"


    def test_stress(self):
        """ Running userprofile stress-tests """

        print("\n-- Initializing stress-test --\n")

        # Set credentials for normal users
        normal_email_head = "test_email"
        normal_email_tail = "@gmail.com"
        normal_credentials = {
            "email": "",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password": "test_password",
            "gender": "Other",
            "gender_other": "test_gender",
            "date_of_birth": "2000-01-01",
            "professional": "User"
        }

        # Generate normal users
        print("Generating " + str(self.n_norm_users) + " normal users...")
        normal_users = []
        for i in range(self.n_norm_users):
            normal_credentials["email"] = normal_email_head + str(i) + normal_email_tail

            # Add tuple of (id, private_key, email, co_prof_user) to list
            user_id, priv_key, _ = registerUser(normal_credentials)
            co_prof_user = int(i // self.n_professionals)
            normal_users.append( (user_id, priv_key.decode("utf-8"), normal_credentials["email"], co_prof_user) )

        # Set credentials for professional users
        prof_email_head = "prof_test_email"
        prof_email_tail = "@gmail.com"
        prof_credentials = {
            "email": "",
            "first_name": "test_prof_first_name",
            "last_name": "test_prof_last_name",
            "password": "test_prof_password",
            "gender": "Other",
            "gender_other": "test_prof_gender",
            "date_of_birth": "2001-01-01",
            "professional": "professional"
        }

        # Generate professional users
        print("Generating " + str(self.n_professionals) + " professional users...")
        prof_users = []
        for i in range(self.n_professionals):
            prof_credentials["email"] = prof_email_head + str(i) + prof_email_tail

            # Add tuple of (id, private_key, email) to list
            user_id, priv_key, _ = registerUser(prof_credentials)
            prof_users.append( (user_id, priv_key.decode("utf-8"), prof_credentials["email"]) )

        # Create relations from each normal to corresponding professional user
        # > Using createRelation(user_id, priv_key, rec_email, perms): bool success
        print("\nCreating relations:")
        for i, user in enumerate(normal_users):
            co_prof_user = int(i // self.n_professionals)
            print("* Relating normal user[" + str(i) + "] to professional user[" + str(co_prof_user) + "], ", end = '')

            # Condition should be 'if not' but isn't due to incomplete coding. Will eventually fail with time
            if createRelation(user[0], user[1], prof_users[co_prof_user][2], self.permissions):
                print("[ERROR] Could not relate normal user[" + str(i) + "] with professional[" + str(co_prof_user) + "]")
                exit(1)

        print("Setup complete")


        print("\n-- Running stress-tests --\n")

        # Stress-test function showAllRelationsFrom()
        # > Using showAllRelationsFrom(receiver_id, receiver_priv_key): list userDict
        print("Measuring operation: showAllRelations() for " + str(self.n_professionals) + " with " + str(self.users_per_professional) + " relations each")
        t0 = time()
        for user in prof_users:
            related_users = showAllRelationsFrom(user[0], user[1])
        t1 = time()
        print("> Resulting time: " + str(t1 - t0) + " seconds")

        print("")

        # Stress-test function updateRelationTo()
        # > Using updateRelationTo(receiver_id, receiver_priv_key): bool success
        print("Measuring operation: updateRelationTo() for " + str(self.n_norm_users) + " users")
        results = []
        t0 = time()
        for user in prof_users:
            updateRelationTo(user[0], user[1])
        t1 = time()
        print("> Result time: " + str(t1 - t0) + " seconds")


        print("\n-- Stress-tests complete --\n")

