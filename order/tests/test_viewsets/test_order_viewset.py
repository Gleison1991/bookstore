def test_order(self):
    response = self.client.get(
        reverse("order-list", kwargs={"version": "v1"}))

    self.assertEqual(response.status_code, status.HTTP_200_OK)

    order_data = json.loads(response.content)
    print("Tipo de order_data:", type(order_data))  # Depuração
    print("Conteúdo de order_data:", order_data)  # Depuração

    if isinstance(order_data, list) and len(order_data) > 0:
        for product in order_data[0]["product"]:
            if product["title"] == self.product.title:
                self.assertEqual(
                    product["title"], self.product.title
                )
                self.assertEqual(
                    product["price"], self.product.price
                )
                self.assertEqual(
                    product["active"], self.product.active
                )
                self.assertEqual(
                    product["category"][0]["title"],
                    self.category.title,
                )

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
