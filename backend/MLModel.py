
class MultiArmedBandit:
    def __init__(self, categories):
        # Initialize the categories, success, and failure counts for each category
        self.categories = categories
        self.successes = {category: 0 for category in categories}  # Number of rewards
        self.failures = {category: 0 for category in categories}   # Number of non-rewards

    def select_category(self):
        best_category = None
        max_sampled_value = float('-inf')  # Start with the smallest possible number

        for category in self.categories:
            # Sample from the Beta distribution for this category
            sampled_value = np.random.beta(self.successes[category] + 1, self.failures[category] + 1)
            
            # Check if the sampled value is the highest we've seen
            if sampled_value > max_sampled_value:
                max_sampled_value = sampled_value
                best_category = category

        return best_category

    def update_values(self, category, reward):
        # Update the success or failure count based on the reward
        if reward > 0:
            self.successes[category] += reward
        else:
            self.failures[category] += 1-reward

    def display_products(self, category):
        # Dummy function to simulate displaying products from a category
        print(f"Displaying products from the highest category: {category}")

# Initialize categories

