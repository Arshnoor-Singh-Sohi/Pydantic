# The Complete Pydantic Guide: From Beginner to Advanced

## Table of Contents
1. [Introduction: What is Pydantic?](#introduction)
2. [Installation and Setup](#installation)
3. [Foundations: Your First Model](#foundations)
4. [Understanding Validation](#validation)
5. [Field Types and Constraints](#field-types)
6. [Working with Optional and Default Values](#optional-defaults)
7. [Nested Models and Complex Structures](#nested-models)
8. [Custom Validation Logic](#custom-validation)
9. [Serialization and Deserialization](#serialization)
10. [Advanced Field Configuration](#advanced-fields)
11. [Model Configuration and Settings](#model-config)
12. [Union Types, Enums, and Literals](#union-enums)
13. [Dynamic Model Creation](#dynamic-models)
14. [Pydantic v1 vs v2: Key Differences](#v1-vs-v2)
15. [Real-World Projects](#projects)
16. [Best Practices and Pitfalls](#best-practices)

---

## 1. Introduction: What is Pydantic? {#introduction}

### The Problem Pydantic Solves

Imagine you're building a REST API that accepts user registration data. Without Pydantic, your code might look like this:

```python
def register_user(data):
    # Manual validation - tedious and error-prone
    if 'email' not in data:
        raise ValueError("Email is required")
    if not isinstance(data['email'], str):
        raise TypeError("Email must be a string")
    if '@' not in data['email']:
        raise ValueError("Invalid email format")
    
    if 'age' not in data:
        raise ValueError("Age is required")
    try:
        age = int(data['age'])
    except (ValueError, TypeError):
        raise ValueError("Age must be a number")
    if age < 0 or age > 120:
        raise ValueError("Age must be between 0 and 120")
    
    # ... and so on for every field
```

This approach is verbose, repetitive, and hard to maintain. You write the same validation patterns everywhere, error messages are inconsistent, and it's easy to forget checks.

Pydantic transforms this into clean, declarative code:

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=120)
```

That's it. Pydantic handles all the validation, type coercion, error messages, and edge cases automatically.

### What Pydantic Does

Pydantic is a data validation library that uses Python type annotations to validate data at runtime. It performs three critical functions:

**Type Enforcement**: Python's type hints are normally just suggestions. Pydantic enforces them. If you declare a field as `int`, Pydantic ensures it's actually an integer or can be safely converted to one.

**Data Validation**: Beyond types, Pydantic validates constraints like minimum values, string patterns, email formats, and custom business rules. You define what valid data looks like, and Pydantic enforces it.

**Data Parsing**: Pydantic automatically converts dictionaries and JSON into typed Python objects. It handles nested structures, optional fields, and complex data hierarchies with minimal code.

### Why Choose Pydantic?

**Runtime Safety**: Unlike type checkers (mypy, pyright) that only work during development, Pydantic validates data when your application runs. This is crucial for external data from APIs, user input, or configuration files.

**Automatic Coercion**: Pydantic is pragmatic. If you pass the string "42" for an integer field, Pydantic converts it rather than failing. This handles real-world messiness while still catching genuine problems.

**Clear Error Messages**: When validation fails, Pydantic provides detailed error messages showing exactly what went wrong and where. This is invaluable for API consumers and debugging.

**IDE Integration**: Because Pydantic uses type hints, modern IDEs provide autocomplete and type checking. You get excellent developer experience with minimal effort.

### When to Use Pydantic

Use Pydantic whenever data crosses boundaries:
- API request and response validation (especially with FastAPI)
- Configuration file parsing (environment variables, YAML, JSON)
- Database model validation (with ORMs or direct queries)
- Data pipeline validation (ETL processes, data transformations)
- Command-line argument parsing
- Webhook payload validation
- Third-party API client libraries

Don't use Pydantic for simple internal data structures where you control all inputs and performance is absolutely critical for millions of validations per second. In those cases, plain dataclasses or named tuples are lighter-weight alternatives.

---

## 2. Installation and Setup {#installation}

### Installing Pydantic

Install Pydantic v2 (the current version) using pip:

```bash
pip install pydantic
```

For additional features like email validation, install the extras:

```bash
pip install 'pydantic[email]'
```

### Version Requirements

Pydantic v2 requires Python 3.8 or newer. Python 3.11+ is recommended for best performance, as Pydantic v2 is built on a Rust core that leverages newer Python optimizations.

### Verifying Installation

Create a simple test file to verify Pydantic works:

```python
from pydantic import BaseModel

class TestModel(BaseModel):
    name: str

# This should work without errors
test = TestModel(name="Alice")
print(test.name)  # Output: Alice
```

---

## 3. Foundations: Your First Model {#foundations}

### Understanding BaseModel

Every Pydantic model inherits from `BaseModel`. This base class provides all the validation magic, serialization methods, and configuration options. Think of `BaseModel` as the foundation that transforms a regular Python class into a validation powerhouse.

### Creating a Simple Model

Let's create a model for a book:

```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    pages: int
    published_year: int

# Creating an instance with valid data
book1 = Book(
    title="1984",
    author="George Orwell",
    pages=328,
    published_year=1949
)

print(book1.title)  # Output: 1984
print(book1.pages)  # Output: 328
```

What's happening here? When you create a `Book` instance, Pydantic validates that all required fields are present and have the correct types. The model definition is declarative—you describe what valid data looks like, and Pydantic handles the rest.

### Type Coercion in Action

Pydantic doesn't just check types; it attempts intelligent conversion:

```python
# Passing string numbers for integer fields
book2 = Book(
    title="Dune",
    author="Frank Herbert",
    pages="412",  # String, but Pydantic converts it
    published_year="1965"  # String, but Pydantic converts it
)

print(type(book2.pages))  # Output: <class 'int'>
print(book2.pages)  # Output: 412
```

This coercion is helpful for real-world scenarios like parsing JSON or URL parameters where everything arrives as strings. Pydantic makes reasonable conversions but will still reject nonsensical data:

```python
try:
    invalid_book = Book(
        title="Invalid",
        author="Test",
        pages="not-a-number",  # Can't convert this to int
        published_year=2000
    )
except Exception as e:
    print(e)
    # Output shows validation error for 'pages' field
```

### Accessing Model Data

Pydantic models work like regular Python objects. You access fields using dot notation:

```python
book = Book(title="Test", author="Author", pages=100, published_year=2020)

# Access as attributes
print(book.title)  # Output: Test

# Modify attributes
book.title = "New Title"
print(book.title)  # Output: New Title

# Convert to dictionary
print(book.model_dump())
# Output: {'title': 'New Title', 'author': 'Author', 'pages': 100, 'published_year': 2020}
```

### Exercise 1: Build Your First Model

Create a `Person` model with the following fields:
- `name`: string
- `age`: integer
- `email`: string
- `is_active`: boolean

Then create instances with both correctly typed data and data that needs coercion (like passing "25" for age). Observe how Pydantic handles both cases.

---

## 4. Understanding Validation {#validation}

### What Happens During Validation

When you create a Pydantic model instance, validation occurs in several stages:

**Stage 1: Type Checking and Coercion**: Pydantic examines each field and attempts to convert the input to the declared type. If the field expects an integer and receives "42", Pydantic converts it. If it receives "hello", conversion fails.

**Stage 2: Field Validation**: After type conversion, Pydantic checks any constraints you've defined (we'll cover these in detail soon). This includes things like minimum/maximum values, string patterns, or custom validation rules.

**Stage 3: Model Validation**: After all fields pass individual validation, model-level validators run. These check relationships between fields or enforce business rules that span multiple values.

### Validation Errors

When validation fails, Pydantic raises a `ValidationError` containing detailed information about what went wrong:

```python
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float
    quantity: int

try:
    product = Product(
        name="Widget",
        price="not-a-number",  # Invalid
        quantity="10"  # Valid (will be coerced)
    )
except ValidationError as e:
    print(e)
    # Shows exactly which field failed and why
```

The error message includes:
- Which field(s) failed validation
- What type was expected
- What value was received
- The specific validation rule that failed

### Understanding Error Structure

Validation errors contain structured data you can parse programmatically:

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    username: str
    age: int
    email: str

try:
    user = User(username="john", age="invalid", email=123)
except ValidationError as e:
    # Get errors as a list of dictionaries
    errors = e.errors()
    for error in errors:
        print(f"Field: {error['loc']}")
        print(f"Error: {error['msg']}")
        print(f"Type: {error['type']}")
        print("---")
```

This structured format is invaluable when building APIs that need to return clear error messages to clients.

### Multiple Errors at Once

Pydantic validates all fields and collects all errors before raising the exception. You don't get one error at a time; you get the complete picture:

```python
try:
    user = User(
        username=123,  # Wrong type
        age="twenty",  # Can't convert to int
        email=None  # Missing value (None isn't valid)
    )
except ValidationError as e:
    print(e)
    # Shows all three validation failures together
```

---

## 5. Field Types and Constraints {#field-types}

### Basic Python Types

Pydantic supports all standard Python types:

```python
from typing import List, Dict, Set, Tuple
from pydantic import BaseModel

class DataTypes(BaseModel):
    # Basic types
    text: str
    number: int
    decimal: float
    flag: bool
    
    # Collections
    tags: List[str]
    metadata: Dict[str, int]
    unique_ids: Set[int]
    coordinates: Tuple[float, float]
```

### Adding Constraints with Field

The `Field` function lets you add validation constraints to your fields:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, le=10000)  # gt = greater than, le = less than or equal
    quantity: int = Field(ge=0)  # ge = greater than or equal
    description: str = Field(default="No description", max_length=500)
    sku: str = Field(pattern=r'^[A-Z]{3}-\d{4}$')  # Regex pattern

# Valid product
product1 = Product(
    name="Laptop",
    price=999.99,
    quantity=50,
    sku="LAP-1234"
)

# Invalid product - price must be greater than 0
try:
    product2 = Product(name="Invalid", price=0, quantity=10, sku="INV-0000")
except ValidationError as e:
    print(e)
```

### Common Field Constraints

Here's a comprehensive overview of available constraints:

**Numeric Constraints:**
- `gt`: greater than
- `ge`: greater than or equal
- `lt`: less than
- `le`: less than or equal
- `multiple_of`: must be a multiple of this value

**String Constraints:**
- `min_length`: minimum string length
- `max_length`: maximum string length
- `pattern`: regex pattern the string must match

**Collection Constraints:**
- `min_length`: minimum number of items
- `max_length`: maximum number of items

### Special String Types

Pydantic provides specialized string types for common formats:

```python
from pydantic import BaseModel, EmailStr, HttpUrl, UUID4
from uuid import uuid4

class UserProfile(BaseModel):
    user_id: UUID4  # Must be a valid UUID4
    email: EmailStr  # Must be a valid email address
    website: HttpUrl  # Must be a valid HTTP/HTTPS URL
    
# Valid data
profile = UserProfile(
    user_id=uuid4(),
    email="user@example.com",
    website="https://example.com"
)

# Invalid email
try:
    profile = UserProfile(
        user_id=uuid4(),
        email="not-an-email",  # Validation fails
        website="https://example.com"
    )
except ValidationError as e:
    print(e)
```

Note: `EmailStr` requires the email-validator package to be installed: `pip install 'pydantic[email]'`

### Constrained Types (Legacy but Still Useful)

Pydantic also offers constrained type classes:

```python
from pydantic import BaseModel, conint, constr, confloat

class StrictProduct(BaseModel):
    # Integer between 0 and 999
    stock: conint(ge=0, le=999)
    
    # String with length constraints
    code: constr(min_length=5, max_length=10, pattern=r'^[A-Z0-9]+$')
    
    # Float with decimal places
    rating: confloat(ge=0.0, le=5.0)

product = StrictProduct(
    stock=100,
    code="ABC123",
    rating=4.5
)
```

In Pydantic v2, using `Field()` is generally preferred over constrained types, but both approaches work.

### Exercise 2: Field Constraints

Create a `BankAccount` model with:
- `account_number`: string, exactly 10 digits
- `balance`: float, must be greater than or equal to 0
- `account_type`: string, must be either "checking" or "savings"
- `overdraft_limit`: float, must be greater than or equal to 0 and less than 10000

Test your model with both valid and invalid data to see the validation errors.

---

## 6. Working with Optional and Default Values {#optional-defaults}

### Understanding Required vs Optional Fields

By default, all fields in a Pydantic model are required. If you create an instance without providing a required field, validation fails:

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str

# This fails - missing 'email'
try:
    user = User(username="john")
except ValidationError as e:
    print(e)
```

### Making Fields Optional with Default Values

The simplest way to make a field optional is to provide a default value:

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    bio: str = "No bio provided"  # Has default, so it's optional
    age: int = 0  # Has default, so it's optional

# This works now - bio and age use defaults
user = User(username="john", email="john@example.com")
print(user.bio)  # Output: No bio provided
print(user.age)  # Output: 0
```

### Optional Fields with None

Sometimes you want a field to be optional but not have a default value—you want it to be `None` if not provided:

```python
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None  # Can be str or None
    age: Optional[int] = None  # Can be int or None

# This works - phone and age are None
user = User(username="john", email="john@example.com")
print(user.phone)  # Output: None

# You can also explicitly set them to None
user2 = User(username="jane", email="jane@example.com", phone=None, age=None)
```

In Python 3.10+, you can use the newer union syntax: `str | None` instead of `Optional[str]`.

### The Difference Between None and Missing

There's an important distinction between a field being `None` and a field being missing entirely:

```python
from typing import Optional
from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    tags: list[str] = Field(default_factory=list)  # Default is empty list

# summary is explicitly None
article1 = Article(title="Test", content="Content", summary=None)
print(article1.summary)  # Output: None

# summary is not provided, defaults to None
article2 = Article(title="Test", content="Content")
print(article2.summary)  # Output: None

# tags uses a factory function to create a new list each time
article3 = Article(title="Test", content="Content")
print(article3.tags)  # Output: []
```

### Using default_factory for Mutable Defaults

Never use mutable default values directly (like `tags: list = []`). This creates a shared mutable object across all instances. Instead, use `default_factory`:

```python
from pydantic import BaseModel, Field

class BlogPost(BaseModel):
    title: str
    comments: list[str] = Field(default_factory=list)  # Correct
    metadata: dict = Field(default_factory=dict)  # Correct

# Each instance gets its own list
post1 = BlogPost(title="First Post")
post1.comments.append("Great!")

post2 = BlogPost(title="Second Post")
print(post2.comments)  # Output: [] (not shared with post1)
```

### Optional vs Required: Design Considerations

When designing your models, think carefully about what should be optional:

**Make fields optional when:**
- They represent truly optional data (like a user's middle name)
- They have sensible defaults (like timestamps that default to "now")
- They're for backward compatibility when adding new fields

**Keep fields required when:**
- The data is essential for your business logic
- Not having the data would cause errors downstream
- You want to catch missing data early

---

## 7. Nested Models and Complex Structures {#nested-models}

### Basic Nested Models

Real-world data is rarely flat. Pydantic excels at validating nested, hierarchical structures:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # Nested model

# Creating an instance with nested data
person = Person(
    name="Alice",
    age=30,
    address={
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "postal_code": "10001"
    }
)

# Access nested fields
print(person.address.city)  # Output: New York
print(person.address.country)  # Output: USA
```

Notice that you can pass a dictionary for the nested `address` field, and Pydantic automatically creates an `Address` instance. This is incredibly powerful for parsing JSON from APIs.

### Lists of Nested Models

You can have lists of complex objects:

```python
from typing import List
from pydantic import BaseModel

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    price: float

class Order(BaseModel):
    order_id: str
    customer_name: str
    items: List[OrderItem]  # List of nested models
    
    def total_price(self) -> float:
        return sum(item.quantity * item.price for item in self.items)

# Creating an order with multiple items
order = Order(
    order_id="ORD-001",
    customer_name="John Doe",
    items=[
        {"product_name": "Widget", "quantity": 2, "price": 9.99},
        {"product_name": "Gadget", "quantity": 1, "price": 19.99},
        {"product_name": "Doohickey", "quantity": 3, "price": 4.99}
    ]
)

print(f"Total: ${order.total_price()}")  # Output: Total: $54.93

# Access individual items
for item in order.items:
    print(f"{item.product_name}: {item.quantity} x ${item.price}")
```

### Deeply Nested Structures

Pydantic handles arbitrary nesting depth:

```python
from typing import List, Optional
from pydantic import BaseModel

class Comment(BaseModel):
    author: str
    text: str
    replies: List['Comment'] = []  # Recursive: comments can have comments

class Post(BaseModel):
    title: str
    content: str
    comments: List[Comment]

# Creating a post with nested comments
post = Post(
    title="Understanding Recursion",
    content="Let me explain...",
    comments=[
        {
            "author": "Alice",
            "text": "Great post!",
            "replies": [
                {
                    "author": "Bob",
                    "text": "I agree!",
                    "replies": []
                }
            ]
        },
        {
            "author": "Charlie",
            "text": "Thanks for sharing",
            "replies": []
        }
    ]
)

# Access deeply nested data
print(post.comments[0].replies[0].author)  # Output: Bob
```

Note the forward reference `'Comment'` in quotes—this allows the model to reference itself before it's fully defined.

### Optional Nested Models

Nested models can be optional too:

```python
from typing import Optional
from pydantic import BaseModel

class ContactInfo(BaseModel):
    email: str
    phone: Optional[str] = None

class Company(BaseModel):
    name: str
    address: Optional[Address] = None  # Entire nested model is optional
    contact: ContactInfo

# Company without an address
company = Company(
    name="Acme Corp",
    contact={"email": "info@acme.com"}
)

print(company.address)  # Output: None
```

### Validation Cascades Through Nesting

When you validate a top-level model, Pydantic validates all nested models:

```python
try:
    invalid_person = Person(
        name="Test",
        age=25,
        address={
            "street": "123 Main",
            "city": "NYC",
            "country": "USA",
            "postal_code": 12345  # Should be string, not int
        }
    )
except ValidationError as e:
    print(e)
    # Error shows it's specifically address.postal_code that failed
```

The error message indicates exactly which nested field failed, making debugging easy even in complex structures.

### Exercise 3: Nested Models

Create models for a simple e-commerce system:
- `Product`: name, price, stock_quantity
- `ShoppingCart`: customer_name, items (list of products with quantities)
- `Customer`: name, email, current_cart (optional ShoppingCart)

Create a customer with a shopping cart containing multiple products, then calculate the total cart value.

---

## 8. Custom Validation Logic {#custom-validation}

### Why Custom Validators?

Field constraints handle common cases (ranges, patterns, etc.), but sometimes you need business-specific validation logic. Maybe a password must contain at least one uppercase letter and one number, or a shipping date must be in the future, or two fields must be consistent with each other. Custom validators handle these scenarios.

### Field Validators

Use the `@field_validator` decorator to add custom validation to specific fields:

```python
from pydantic import BaseModel, field_validator
from datetime import datetime

class Event(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Event name cannot be empty or whitespace')
        return v.strip()  # Return the cleaned value
    
    @field_validator('end_date')
    @classmethod
    def end_after_start(cls, v, info):
        # info.data contains other field values validated so far
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('End date must be after start date')
        return v

# Valid event
event1 = Event(
    name="Conference",
    start_date=datetime(2025, 6, 1),
    end_date=datetime(2025, 6, 3)
)

# Invalid - end before start
try:
    event2 = Event(
        name="Invalid Event",
        start_date=datetime(2025, 6, 3),
        end_date=datetime(2025, 6, 1)
    )
except ValidationError as e:
    print(e)
```

Key points about field validators:
- They must be class methods (use `@classmethod`)
- The first parameter after `cls` is the value being validated
- The optional `info` parameter provides context about other fields
- Return the validated (and possibly transformed) value
- Raise `ValueError` with a clear message if validation fails

### Validating Multiple Fields

You can apply one validator to multiple fields:

```python
from pydantic import BaseModel, field_validator

class Rectangle(BaseModel):
    width: float
    height: float
    
    @field_validator('width', 'height')
    @classmethod
    def dimensions_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Dimensions must be positive')
        return v

# Valid rectangle
rect = Rectangle(width=10.5, height=5.2)

# Invalid - negative dimension
try:
    invalid_rect = Rectangle(width=-5, height=10)
except ValidationError as e:
    print(e)
```

### Model Validators

Sometimes you need to validate relationships between multiple fields or perform validation that depends on the entire model. Use `@model_validator`:

```python
from pydantic import BaseModel, model_validator

class DiscountedProduct(BaseModel):
    name: str
    original_price: float
    discount_percent: float
    final_price: float
    
    @model_validator(mode='after')
    def check_final_price(self):
        expected_price = self.original_price * (1 - self.discount_percent / 100)
        if abs(self.final_price - expected_price) > 0.01:  # Allow small rounding errors
            raise ValueError(
                f'Final price {self.final_price} does not match expected '
                f'{expected_price:.2f} with {self.discount_percent}% discount'
            )
        return self

# Valid product
product = DiscountedProduct(
    name="Widget",
    original_price=100.0,
    discount_percent=20,
    final_price=80.0
)

# Invalid - final price doesn't match discount
try:
    invalid_product = DiscountedProduct(
        name="Gadget",
        original_price=100.0,
        discount_percent=20,
        final_price=85.0  # Should be 80
    )
except ValidationError as e:
    print(e)
```

Model validators have two modes:
- `mode='before'`: Runs before field validation, receives raw input data
- `mode='after'`: Runs after field validation, receives a model instance

### Before vs After Validators

The `mode` parameter controls when your validator runs:

```python
from pydantic import BaseModel, model_validator

class DataCleaner(BaseModel):
    values: list[int]
    
    @model_validator(mode='before')
    @classmethod
    def clean_input(cls, data):
        # Runs on raw input before field validation
        # data is a dict (or whatever was passed in)
        if 'values' in data and isinstance(data['values'], str):
            # Convert comma-separated string to list
            data['values'] = [int(x.strip()) for x in data['values'].split(',')]
        return data
    
    @model_validator(mode='after')
    def remove_duplicates(self):
        # Runs after field validation
        # self is a model instance
        self.values = list(set(self.values))
        return self

# This works - before validator preprocesses the input
cleaner = DataCleaner(values="1,2,3,2,1")
print(cleaner.values)  # Output: [1, 2, 3] (duplicates removed)
```

Use `mode='before'` to transform or clean raw input data before validation. Use `mode='after'` to validate relationships or transform data after individual fields are validated.

### Reusable Validators

You can create validator functions outside models and reuse them:

```python
from pydantic import BaseModel, field_validator

def validate_positive(v):
    if v <= 0:
        raise ValueError('Must be positive')
    return v

class Product(BaseModel):
    price: float
    stock: int
    
    _validate_price = field_validator('price')(classmethod(validate_positive))
    _validate_stock = field_validator('stock')(classmethod(validate_positive))

class Transaction(BaseModel):
    amount: float
    
    _validate_amount = field_validator('amount')(classmethod(validate_positive))
```

This pattern reduces duplication when you have common validation logic across multiple models.

### Exercise 4: Custom Validators

Create a `UserRegistration` model with:
- `username`: 5-20 characters, alphanumeric only
- `password`: minimum 8 characters, must contain uppercase, lowercase, and number
- `confirm_password`: must match password
- `age`: must be 18 or older
- `email`: valid email format

Implement custom validators for password strength and password confirmation matching.

---

## 9. Serialization and Deserialization {#serialization}

### Converting Models to Dictionaries

Pydantic models can be easily converted back to Python dictionaries:

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    age: int

user = User(username="alice", email="alice@example.com", age=30)

# Convert to dictionary
user_dict = user.model_dump()
print(user_dict)
# Output: {'username': 'alice', 'email': 'alice@example.com', 'age': 30}
```

The `model_dump()` method (called `dict()` in Pydantic v1) converts the model to a dictionary, which is useful for passing data to functions, storing in databases, or serializing to JSON.

### Excluding Fields

You can exclude specific fields from serialization:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    email: str
    password: str
    age: int

user = User(username="alice", email="alice@example.com", password="secret123", age=30)

# Exclude password from output
safe_dict = user.model_dump(exclude={'password'})
print(safe_dict)
# Output: {'username': 'alice', 'email': 'alice@example.com', 'age': 30}

# Include only specific fields
minimal_dict = user.model_dump(include={'username', 'email'})
print(minimal_dict)
# Output: {'username': 'alice', 'email': 'alice@example.com'}
```

### Excluding Fields by Configuration

You can also configure fields to be excluded by default:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    email: str
    password: str = Field(exclude=True)  # Never included in dumps
    internal_id: int = Field(exclude=True)

user = User(username="alice", email="alice@example.com", password="secret", internal_id=12345)

# Password and internal_id are automatically excluded
print(user.model_dump())
# Output: {'username': 'alice', 'email': 'alice@example.com'}
```

### Converting to JSON

Pydantic can serialize models directly to JSON strings:

```python
from datetime import datetime
from pydantic import BaseModel

class Event(BaseModel):
    name: str
    timestamp: datetime
    attendees: list[str]

event = Event(
    name="Team Meeting",
    timestamp=datetime(2025, 10, 3, 10, 0),
    attendees=["Alice", "Bob", "Charlie"]
)

# Convert to JSON string
json_str = event.model_dump_json()
print(json_str)
# Output: {"name":"Team Meeting","timestamp":"2025-10-03T10:00:00",...}

# Pretty-printed JSON
json_str_pretty = event.model_dump_json(indent=2)
print(json_str_pretty)
```

Note how Pydantic automatically handles datetime serialization to ISO format. This is much cleaner than manually handling datetime serialization with the standard `json` module.

### Parsing from JSON and Dictionaries

The reverse operation—creating models from dictionaries or JSON—is equally straightforward:

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float

# From dictionary (what we've been doing all along)
product1 = Product(**{"name": "Widget", "price": 9.99})

# From JSON string
json_data = '{"name": "Gadget", "price": 19.99}'
product2 = Product.model_validate_json(json_data)

print(product2.name)  # Output: Gadget
print(product2.price)  # Output: 19.99
```

The `model_validate_json()` method parses a JSON string and validates it in one step, raising `ValidationError` if the data is invalid.

### Handling Nested Models in Serialization

Nested models are automatically handled during serialization:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str

class Person(BaseModel):
    name: str
    address: Address

person = Person(
    name="Alice",
    address={"street": "123 Main St", "city": "NYC"}
)

# Nested models are fully serialized
print(person.model_dump())
# Output: {'name': 'Alice', 'address': {'street': '123 Main St', 'city': 'NYC'}}

# Works with JSON too
print(person.model_dump_json())
```

### Serialization Aliases

You can configure different names for serialization vs internal use:

```python
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    user_name: str = Field(serialization_alias='userName')
    email_address: str = Field(serialization_alias='emailAddress')

response = APIResponse(user_name="alice", email_address="alice@example.com")

# Serializes with camelCase aliases
print(response.model_dump(by_alias=True))
# Output: {'userName': 'alice', 'emailAddress': 'alice@example.com'}

# Without by_alias, uses field names
print(response.model_dump())
# Output: {'user_name': 'alice', 'email_address': 'alice@example.com'}
```

This is particularly useful when working with external APIs that use different naming conventions than your Python code (e.g., camelCase vs snake_case).

---

## 10. Advanced Field Configuration {#advanced-fields}

### Aliasing: Multiple Names for Fields

Sometimes external data uses different field names than you want in your code. Pydantic supports input aliasing:

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    name: str
    email_address: str = Field(validation_alias='email')
    phone_number: str = Field(validation_alias='phone')

# Can use either the field name or the alias during creation
profile1 = UserProfile(name="Alice", email="alice@example.com", phone="555-1234")
profile2 = UserProfile(name="Bob", email_address="bob@example.com", phone_number="555-5678")

# Internal field names are always used for access
print(profile1.email_address)  # Output: alice@example.com
print(profile2.phone_number)  # Output: 555-5678
```

This allows you to accept data in one format but work with it using more convenient names internally.

### Computed Fields

Sometimes you want fields that are calculated from other fields rather than provided as input:

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float
    
    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height
    
    @computed_field
    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

rect = Rectangle(width=10, height=5)

# Computed fields work like regular fields
print(rect.area)  # Output: 50.0
print(rect.perimeter)  # Output: 30.0

# They're included in serialization
print(rect.model_dump())
# Output: {'width': 10.0, 'height': 5.0, 'area': 50.0, 'perimeter': 30.0}
```

Computed fields are read-only and calculated on-the-fly. They're included in serialization by default but can be excluded with configuration.

### Field Descriptions and Metadata

You can add documentation to fields that appears in schema generation and error messages:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(description="The product's display name")
    sku: str = Field(
        description="Stock keeping unit - unique product identifier",
        examples=["PROD-001", "WIDGET-42"]
    )
    price: float = Field(
        description="Price in USD",
        gt=0,
        examples=[9.99, 149.99]
    )

# Generate JSON schema (useful for API documentation)
schema = Product.model_json_schema()
print(schema)
```

This metadata is invaluable when generating API documentation (e.g., with FastAPI) or creating user interfaces.

### Private Fields

Fields starting with underscore are treated as private and excluded from validation/serialization:

```python
from pydantic import BaseModel, PrivateAttr

class User(BaseModel):
    username: str
    email: str
    _internal_id: int = PrivateAttr(default=0)  # Private attribute
    
user = User(username="alice", email="alice@example.com")
user._internal_id = 12345  # Can set after creation

print(user.model_dump())
# Output: {'username': 'alice', 'email': 'alice@example.com'}
# _internal_id is not included
```

Private attributes are useful for caching, internal state, or data that shouldn't be part of the external interface.

### Frozen Models

Make models immutable by using frozen configuration:

```python
from pydantic import BaseModel, ConfigDict

class ImmutablePoint(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    x: float
    y: float

point = ImmutablePoint(x=10, y=20)

# Attempting to modify raises an error
try:
    point.x = 15
except ValidationError as e:
    print("Cannot modify frozen model")
```

Frozen models are useful for representing values that shouldn't change after creation, like coordinates, configuration settings, or database records that represent historical data.

---

## 11. Model Configuration and Settings {#model-config}

### Model Config

Pydantic v2 uses `model_config` with `ConfigDict` to control model behavior:

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace from strings
        str_min_length=1,  # Global min length for all strings
        validate_default=True,  # Validate default values
        frozen=False,  # Allow modifications
        extra='forbid'  # Don't allow extra fields
    )
    
    username: str
    email: str

# Whitespace is automatically stripped
user = User(username="  alice  ", email="  alice@example.com  ")
print(user.username)  # Output: "alice" (no whitespace)

# Extra fields cause errors
try:
    invalid_user = User(
        username="bob",
        email="bob@example.com",
        age=25  # Not defined in model
    )
except ValidationError as e:
    print(e)  # Error: extra fields not permitted
```

### Controlling Extra Fields

The `extra` config option controls what happens when unexpected fields are provided:

```python
from pydantic import BaseModel, ConfigDict

# Forbid extra fields (strict)
class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str

# Ignore extra fields (default)
class IgnoreExtraModel(BaseModel):
    model_config = ConfigDict(extra='ignore')
    name: str

# Allow extra fields
class AllowExtraModel(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str

# Strict: raises error
try:
    StrictModel(name="test", age=25)
except ValidationError:
    print("Extra fields not allowed")

# Ignore: silently drops extra fields
model2 = IgnoreExtraModel(name="test", age=25)
print(model2.model_dump())  # Output: {'name': 'test'}

# Allow: keeps extra fields
model3 = AllowExtraModel(name="test", age=25)
print(model3.model_dump())  # Output: {'name': 'test', 'age': 25}
print(model3.age)  # Can access extra fields dynamically
```

### Strict Mode

Pydantic v2 introduced strict mode, which disables type coercion:

```python
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)
    
    age: int
    name: str

# With strict mode, type coercion is disabled
try:
    # This would work in non-strict mode (coerces "25" to 25)
    user = StrictModel(age="25", name="Alice")
except ValidationError as e:
    print(e)  # Error: Input should be a valid integer

# Must provide exact types
user = StrictModel(age=25, name="Alice")  # This works
```

Strict mode is useful when you want to ensure data comes in exactly the right format with no automatic conversions.

### Customizing Field Ordering

You can control how fields appear in serialization:

```python
from pydantic import BaseModel

class User(BaseModel):
    email: str
    username: str
    age: int

# Fields appear in definition order
user = User(username="alice", age=30, email="alice@example.com")
print(user.model_dump())
# Output: {'email': '...', 'username': '...', 'age': ...}
```

Field order in the class definition determines serialization order, which can be important for APIs or display logic.

---

## 12. Union Types, Enums, and Literals {#union-enums}

### Union Types

Sometimes a field can accept multiple types. Use Python's `Union` type (or the `|` operator in Python 3.10+):

```python
from typing import Union
from pydantic import BaseModel

class FlexibleID(BaseModel):
    id: Union[int, str]  # Can be either int or str
    name: str

# Both work
item1 = FlexibleID(id=12345, name="Numeric ID")
item2 = FlexibleID(id="ABC-123", name="String ID")

print(item1.id)  # Output: 12345 (int)
print(item2.id)  # Output: ABC-123 (str)

# Python 3.10+ syntax
class ModernFlexibleID(BaseModel):
    id: int | str
    name: str
```

Pydantic tries each type in order until one validates successfully. This is useful for APIs that accept flexible input formats.

### Union Validation Order Matters

When using unions, order matters:

```python
from pydantic import BaseModel

class Example(BaseModel):
    value: int | str  # Tries int first, then str

# "42" is coerced to int
ex1 = Example(value="42")
print(type(ex1.value))  # Output: <class 'int'>

# If you want it to stay as string, put str first
class StringFirst(BaseModel):
    value: str | int

ex2 = StringFirst(value="42")
print(type(ex2.value))  # Output: <class 'str'>
```

### Enums for Restricted Choices

Use Python's `Enum` for fields that must be one of a fixed set of values:

```python
from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(BaseModel):
    applicant_name: str
    status: Status

# Valid statuses
app1 = Application(applicant_name="Alice", status=Status.PENDING)
app2 = Application(applicant_name="Bob", status="approved")  # String works too

print(app1.status)  # Output: Status.PENDING
print(app1.status.value)  # Output: "pending"

# Invalid status
try:
    app3 = Application(applicant_name="Charlie", status="invalid")
except ValidationError as e:
    print(e)  # Error: status must be one of the valid enum values
```

Enums are perfect for status fields, categories, or any field with a fixed set of allowed values.

### Literal Types for Exact Values

For even simpler cases with just a few literal values, use `Literal`:

```python
from typing import Literal
from pydantic import BaseModel

class HttpResponse(BaseModel):
    status: Literal["success", "error", "pending"]
    message: str

# Valid
response1 = HttpResponse(status="success", message="Operation completed")
response2 = HttpResponse(status="error", message="Something went wrong")

# Invalid - not one of the literal values
try:
    response3 = HttpResponse(status="unknown", message="Test")
except ValidationError as e:
    print(e)
```

`Literal` is simpler than `Enum` when you don't need the additional structure or methods that enums provide.

### Discriminated Unions

For complex unions of different models, discriminated unions make validation more efficient and error messages clearer:

```python
from typing import Literal, Union
from pydantic import BaseModel, Field

class Cat(BaseModel):
    pet_type: Literal["cat"]
    meow_volume: int

class Dog(BaseModel):
    pet_type: Literal["dog"]
    bark_volume: int

class Pet(BaseModel):
    pet: Union[Cat, Dog] = Field(discriminator='pet_type')

# Pydantic uses pet_type to determine which model to validate
cat = Pet(pet={"pet_type": "cat", "meow_volume": 5})
dog = Pet(pet={"pet_type": "dog", "bark_volume": 8})

print(type(cat.pet))  # Output: <class 'Cat'>
print(type(dog.pet))  # Output: <class 'Dog'>
```

The discriminator field (`pet_type`) tells Pydantic which model to use, making validation faster and error messages more precise.

### Exercise 5: Unions and Enums

Create an event tracking system with:
- `EventType` enum: login, logout, purchase, error
- `Event` model with:
  - `event_id`: int or string
  - `event_type`: EventType
  - `user_id`: int
  - `details`: dict
- Create various events and demonstrate both ID types work

---

## 13. Dynamic Model Creation {#dynamic-models}

### Creating Models at Runtime

Sometimes you need to create models programmatically based on configuration or runtime data. Pydantic's `create_model` function enables this:

```python
from pydantic import create_model, Field

# Create a model dynamically
DynamicUser = create_model(
    'DynamicUser',
    username=(str, ...),  # ... means required
    email=(str, Field(description="User's email")),
    age=(int, Field(default=0, ge=0)),
)

# Use it like any other model
user = DynamicUser(username="alice", email="alice@example.com")
print(user.username)  # Output: alice
```

The tuple format is: `(type, default_or_field)`. Use `...` (ellipsis) for required fields.

### Dynamic Fields from Configuration

Here's a practical example—creating a model based on a configuration schema:

```python
from pydantic import create_model, Field

def create_config_model(schema):
    """
    Create a Pydantic model from a schema dictionary.
    
    schema format:
    {
        'field_name': {
            'type': str/int/float/bool,
            'required': True/False,
            'default': value,
            'description': "..."
        }
    }
    """
    fields = {}
    for field_name, field_config in schema.items():
        field_type = field_config['type']
        required = field_config.get('required', True)
        default = field_config.get('default', ...)
        description = field_config.get('description', '')
        
        if required:
            fields[field_name] = (field_type, Field(description=description))
        else:
            fields[field_name] = (field_type, Field(default=default, description=description))
    
    return create_model('DynamicConfigModel', **fields)

# Define schema
schema = {
    'api_key': {
        'type': str,
        'required': True,
        'description': 'API authentication key'
    },
    'timeout': {
        'type': int,
        'required': False,
        'default': 30,
        'description': 'Request timeout in seconds'
    },
    'debug': {
        'type': bool,
        'required': False,
        'default': False,
        'description': 'Enable debug mode'
    }
}

# Create model from schema
ConfigModel = create_config_model(schema)

# Use it
config = ConfigModel(api_key="secret-key-123")
print(config.timeout)  # Output: 30 (default)
print(config.debug)  # Output: False (default)
```

### Adding Methods to Dynamic Models

Dynamic models can have methods too:

```python
from pydantic import create_model

def calculate_total(self):
    return self.price * self.quantity

DynamicProduct = create_model(
    'DynamicProduct',
    name=(str, ...),
    price=(float, ...),
    quantity=(int, ...),
    __module__=__name__,  # Set module for better repr
    calculate_total=calculate_total  # Add method
)

product = DynamicProduct(name="Widget", price=9.99, quantity=5)
print(product.calculate_total())  # Output: 49.95
```

### When to Use Dynamic Models

Dynamic model creation is powerful but should be used judiciously. Good use cases include:

- Building frameworks or libraries where models are defined by users
- Creating models from API schemas or OpenAPI specifications
- Generating validation models from database schemas
- Building configuration systems where fields are defined in config files

For normal application code where models are known at development time, define them statically for better type checking and IDE support.

---

## 14. Pydantic v1 vs v2: Key Differences {#v1-vs-v2}

### Major Changes in Pydantic v2

Pydantic v2, released in 2023, represents a major rewrite with significant performance improvements and some breaking changes. If you're working with existing code or migrating from v1, here are the key differences:

### Config Class vs ConfigDict

**V1 approach:**
```python
from pydantic import BaseModel

class UserV1(BaseModel):
    username: str
    email: str
    
    class Config:
        str_strip_whitespace = True
        frozen = False
```

**V2 approach:**
```python
from pydantic import BaseModel, ConfigDict

class UserV2(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        frozen=False
    )
    
    username: str
    email: str
```

### Serialization Methods

**V1 methods:**
- `.dict()` → convert to dictionary
- `.json()` → convert to JSON string
- `.parse_obj()` → create from dictionary
- `.parse_raw()` → create from JSON string

**V2 methods:**
- `.model_dump()` → convert to dictionary
- `.model_dump_json()` → convert to JSON string
- `.model_validate()` → create from dictionary
- `.model_validate_json()` → create from JSON string

Example migration:

```python
# V1 style
user_dict = user.dict()
user_json = user.json()
new_user = User.parse_obj(data)

# V2 style
user_dict = user.model_dump()
user_json = user.model_dump_json()
new_user = User.model_validate(data)
```

### Validator Decorators

**V1 validators:**
```python
from pydantic import BaseModel, validator

class UserV1(BaseModel):
    email: str
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v
```

**V2 validators:**
```python
from pydantic import BaseModel, field_validator

class UserV2(BaseModel):
    email: str
    
    @field_validator('email')
    @classmethod
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v
```

Note the `@classmethod` decorator is now required in v2.

### Root Validators

**V1 root validators:**
```python
from pydantic import BaseModel, root_validator

class ModelV1(BaseModel):
    field1: int
    field2: int
    
    @root_validator
    def check_fields(cls, values):
        if values['field1'] > values['field2']:
            raise ValueError('field1 must be <= field2')
        return values
```

**V2 model validators:**
```python
from pydantic import BaseModel, model_validator

class ModelV2(BaseModel):
    field1: int
    field2: int
    
    @model_validator(mode='after')
    def check_fields(self):
        if self.field1 > self.field2:
            raise ValueError('field1 must be <= field2')
        return self
```

### Performance Improvements

Pydantic v2 is significantly faster than v1 (typically 5-50x depending on the use case) because the core validation logic is now written in Rust. For most applications, this means:

- Faster API request validation
- Quicker data processing in ETL pipelines
- Lower CPU usage in production

### Migration Strategy

If you're migrating from v1 to v2:

1. Install the compatibility library: `pip install pydantic[v1]`
2. This allows v1 code to run alongside v2 code
3. Migrate models incrementally, testing thoroughly
4. Use the migration guide at docs.pydantic.dev for complex cases

For new projects, start with v2 from the beginning—there's no reason to use v1 anymore unless you're maintaining legacy code.

---

## 15. Real-World Projects {#projects}

### Project 1: FastAPI with Pydantic Validation

FastAPI uses Pydantic extensively for request/response validation. Here's a complete example:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI()

class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    age: Optional[int] = Field(None, ge=13, le=120)

class UserResponse(BaseModel):
    """Model for user responses (no password)"""
    id: int
    username: str
    email: EmailStr
    age: Optional[int]

# Simulated database
fake_db = {}
next_id = 1

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    Pydantic automatically validates:
    - username length (3-50 chars)
    - email format
    - password length (min 8 chars)
    - age range (13-120) if provided
    """
    global next_id
    
    # Check if username exists
    if any(u['username'] == user.username for u in fake_db.values()):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Store user (in real app, hash password first!)
    user_id = next_id
    fake_db[user_id] = user.model_dump()
    next_id += 1
    
    # Return response (password excluded by UserResponse model)
    return UserResponse(
        id=user_id,
        username=user.username,
        email=user.email,
        age=user.age
    )

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a user by ID"""
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = fake_db[user_id].copy()
    user_data['id'] = user_id
    return UserResponse(**user_data)
```

Key points:
- Separate models for input (`UserCreate`) and output (`UserResponse`)
- Password is excluded from responses automatically
- Validation happens automatically before handler executes
- Invalid data returns clear 422 error with details

### Project 2: Configuration Management

Pydantic Settings makes configuration management type-safe and validated:

```python
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn

class AppSettings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    
    Set variables like:
    export APP_NAME="MyApp"
    export DEBUG="true"
    export DATABASE_URL="postgresql://user:pass@localhost/dbname"
    """
    
    app_name: str = Field(default="MyApp")
    debug: bool = Field(default=False)
    database_url: PostgresDsn
    secret_key: str = Field(min_length=32)
    max_connections: int = Field(default=10, ge=1, le=100)
    
    model_config = ConfigDict(
        env_file='.env',  # Load from .env file
        env_file_encoding='utf-8'
    )

# Load settings - reads from environment variables and .env file
settings = AppSettings()

print(f"App: {settings.app_name}")
print(f"Debug mode: {settings.debug}")
print(f"Max connections: {settings.max_connections}")
```

Benefits:
- Type-safe configuration access
- Validation ensures all required settings are present
- Automatic coercion (string "true" becomes boolean True)
- Clear errors if configuration is invalid

### Project 3: Data Validation Pipeline

Processing CSV data with validation:

```python
from pydantic import BaseModel, Field, ValidationError
from typing import List
import csv
from datetime import datetime

class SalesRecord(BaseModel):
    """Validated sales record from CSV"""
    order_id: str = Field(pattern=r'^ORD-\d{6}$')
    customer_email: EmailStr
    product_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    order_date: datetime
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price

def process_sales_csv(filename: str) -> tuple[List[SalesRecord], List[dict]]:
    """
    Process sales CSV with validation.
    
    Returns:
        - List of valid records
        - List of invalid records with errors
    """
    valid_records = []
    invalid_records = []
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            try:
                record = SalesRecord(**row)
                valid_records.append(record)
            except ValidationError as e:
                invalid_records.append({
                    'row': row_num,
                    'data': row,
                    'errors': e.errors()
                })
    
    return valid_records, invalid_records

# Usage
valid, invalid = process_sales_csv('sales.csv')

print(f"Valid records: {len(valid)}")
print(f"Invalid records: {len(invalid)}")

# Calculate total sales from valid records
total_sales = sum(record.total_price for record in valid)
print(f"Total sales: ${total_sales:,.2f}")

# Report errors
for error_record in invalid:
    print(f"\nRow {error_record['row']} errors:")
    for error in error_record['errors']:
        print(f"  - {error['loc'][0]}: {error['msg']}")
```

This pattern is powerful for ETL pipelines—you get comprehensive error reporting while processing valid records.

### Project 4: API Client with Type Safety

Building a type-safe API client:

```python
from pydantic import BaseModel
from typing import List
import requests

class Repository(BaseModel):
    """GitHub repository model"""
    id: int
    name: str
    full_name: str
    description: str | None
    stars: int = Field(validation_alias='stargazers_count')
    forks: int = Field(validation_alias='forks_count')
    language: str | None

class GitHubClient:
    """Type-safe GitHub API client using Pydantic"""
    
    BASE_URL = "https://api.github.com"
    
    def get_user_repos(self, username: str) -> List[Repository]:
        """
        Get all repositories for a user.
        
        Returns validated Repository objects.
        """
        response = requests.get(f"{self.BASE_URL}/users/{username}/repos")
        response.raise_for_status()
        
        # Pydantic validates each repository
        repos_data = response.json()
        repos = [Repository(**repo) for repo in repos_data]
        
        return repos
    
    def get_popular_repos(self, username: str, min_stars: int = 100) -> List[Repository]:
        """Get user's repositories with at least min_stars"""
        all_repos = self.get_user_repos(username)
        return [repo for repo in all_repos if repo.stars >= min_stars]

# Usage
client = GitHubClient()
repos = client.get_popular_repos("pydantic", min_stars=100)

for repo in repos:
    print(f"{repo.name}: {repo.stars} stars ({repo.language})")
```

Benefits:
- Automatic validation of API responses
- Type safety—your IDE knows the structure
- Clear errors if API response format changes
- Alias handling for different naming conventions

---

## 16. Best Practices and Common Pitfalls {#best-practices}

### Best Practices

**1. Use Specific Types**

Instead of generic types, use the most specific type that fits:

```python
# Less specific
class User(BaseModel):
    email: str  # Any string

# More specific
from pydantic import EmailStr

class User(BaseModel):
    email: EmailStr  # Validates email format
```

**2. Separate Input and Output Models**

Especially in APIs, use different models for requests and responses:

```python
class UserCreate(BaseModel):
    """For creating users"""
    username: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    """For returning user data"""
    id: int
    username: str
    email: EmailStr
    # No password field!
```

**3. Use Validators for Business Logic**

Keep business rules in validators:

```python
class Order(BaseModel):
    items: List[OrderItem]
    discount_code: Optional[str]
    
    @model_validator(mode='after')
    def validate_discount(self):
        if self.discount_code and not self.items:
            raise ValueError("Cannot apply discount to empty order")
        return self
```

**4. Document Your Models**

Use field descriptions and docstrings:

```python
class Product(BaseModel):
    """
    Represents a product in the catalog.
    
    Products must have positive prices and valid SKUs.
    """
    name: str = Field(description="Product display name")
    sku: str = Field(description="Stock keeping unit", pattern=r'^[A-Z]{3}-\d{4}$')
    price: float = Field(description="Price in USD", gt=0)
```

### Common Pitfalls

**1. Mutable Defaults**

Never use mutable objects as defaults:

```python
# WRONG - all instances share the same list!
class BadModel(BaseModel):
    tags: list = []

# CORRECT - each instance gets a new list
class GoodModel(BaseModel):
    tags: list = Field(default_factory=list)
```

**2. Forgetting Optional Types**

If a field can be `None`, declare it as `Optional`:

```python
# WRONG - will fail if middle_name is None
class Person(BaseModel):
    first_name: str
    middle_name: str  # Doesn't allow None
    last_name: str

# CORRECT
class Person(BaseModel):
    first_name: str
    middle_name: Optional[str] = None  # Allows None
    last_name: str
```

**3. Overusing Validators**

Don't use validators for simple constraints that Field can handle:

```python
# Unnecessary validator
class Product(BaseModel):
    price: float
    
    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

# Better - use Field constraints
class Product(BaseModel):
    price: float = Field(gt=0)
```

**4. Ignoring Validation Errors**

Always handle `ValidationError` appropriately:

```python
# Bad - silent failure
try:
    user = User(**data)
except ValidationError:
    user = None  # What went wrong?

# Good - informative handling
try:
    user = User(**data)
except ValidationError as e:
    print(f"Validation failed: {e}")
    # Log errors, return to client, etc.
```

### Performance Considerations

**1. Avoid Unnecessary Validation**

If you're creating many models from trusted internal data, consider bypassing validation:

```python
# Normal validation (use for external data)
user = User(**data)

# Skip validation (use only for trusted internal data)
user = User.model_construct(**data)
```

**2. Reuse Model Instances**

Creating model instances has overhead. For high-frequency operations, consider validation once and reusing:

```python
# Validate once
config = AppConfig(**config_data)

# Reuse throughout application lifetime
for i in range(1000000):
    # Use config.database_url, etc.
    pass
```

**3. Use Frozen Models for Immutable Data**

Frozen models can be cached and hashed:

```python
class Coordinate(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    latitude: float
    longitude: float

# Can use as dict key
cache = {Coordinate(lat=40.7, lon=-74.0): "New York"}
```

### When NOT to Use Pydantic

Pydantic isn't always the right tool:

**Don't use Pydantic when:**
- Working entirely with internal, trusted data structures
- Performance is critical for millions of operations per second
- You need the absolute lightest-weight data containers (use dataclasses or NamedTuples)
- The validation overhead isn't justified by the benefits

**Do use Pydantic when:**
- Data crosses boundaries (APIs, files, user input)
- You need clear validation errors
- Type safety and IDE support are valuable
- You're building libraries or frameworks

### Summary of Key Concepts

Throughout this guide, you've learned:

1. **Validation**: Pydantic enforces types and constraints at runtime
2. **Coercion**: Pragmatic type conversion for real-world data
3. **Nested Models**: Hierarchical data structures with full validation
4. **Custom Validators**: Business logic validation with clear errors
5. **Serialization**: Easy conversion to/from dicts and JSON
6. **Configuration**: Type-safe settings management
7. **Integration**: Works beautifully with FastAPI, ORMs, and other tools

Pydantic is about making Python more robust when handling external data. It catches errors early, provides clear feedback, and makes your code more maintainable. Use it wisely, and it becomes an indispensable tool in your Python toolkit.

### Next Steps

To continue your Pydantic journey:
- Explore the official docs at docs.pydantic.dev
- Build a FastAPI application using Pydantic models
- Implement configuration management with Pydantic Settings
- Contribute to open-source projects using Pydantic
- Practice by validating real-world data sources in your projects

Happy validating!
